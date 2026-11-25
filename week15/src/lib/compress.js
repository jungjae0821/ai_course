// 사진을 목표 용량 이하로 줄인다. 모든 처리는 브라우저 안에서 일어난다.
//
// 1단계: 해상도는 그대로 두고 품질만 낮춘다.
// 2단계: 품질을 MIN_QUALITY까지 낮춰도 안 되면, 가로세로 비율을 지키며 해상도를 단계적으로 줄인다.
//        줄인 해상도에서는 다시 목표 안에서 가장 높은 품질을 찾는다.

export const FORMATS = {
  jpg: { mime: 'image/jpeg', label: 'JPG', lossy: true },
  webp: { mime: 'image/webp', label: 'WebP', lossy: true },
  png: { mime: 'image/png', label: 'PNG', lossy: false },
};

const MAX_QUALITY = 0.92;
// 이보다 낮추면 뭉개짐이 눈에 띄어서, 품질을 더 깎는 대신 해상도를 줄인다.
const MIN_QUALITY = 0.6;
// 모바일 Safari의 캔버스 한계(약 1,670만 픽셀)보다 조금 작게 잡는다.
const MAX_AREA = 16_000_000;
const MIN_SIDE = 32;
const QUALITY_SEARCH_STEPS = 6;

const MIME_TO_KEY = { 'image/jpeg': 'jpg', 'image/webp': 'webp', 'image/png': 'png' };

/** 올린 파일의 확장자. key는 이 앱이 만들 수 있는 형식일 때만 채워진다. */
export function formatOf(file) {
  const key = MIME_TO_KEY[file.type] ?? null;
  if (key) return { key, label: FORMATS[key].label };
  const fromType = file.type.startsWith('image/') ? file.type.slice(6).split('+')[0] : '';
  const fromName = file.name.includes('.') ? file.name.split('.').pop() : '';
  return { key: null, label: (fromType || fromName || '알 수 없음').toUpperCase() };
}

export function formatBytes(bytes) {
  const kb = bytes / 1024;
  // 반올림한 뒤에 비교해야 999.6KB가 "1000KB"로 나오지 않는다.
  const shown = kb < 10 ? Number(kb.toFixed(1)) : Math.round(kb);
  if (shown < 1000) return `${kb < 10 ? kb.toFixed(1) : shown}KB`;
  return `${(kb / 1024).toFixed(1)}MB`;
}

/** image.jpg → image_compressed.jpg */
export function outputName(originalName, formatKey) {
  const dot = originalName.lastIndexOf('.');
  const base = dot > 0 ? originalName.slice(0, dot) : originalName;
  return `${base}_compressed.${formatKey}`;
}

export async function loadSource(file) {
  let image;
  try {
    image = await createImageBitmap(file, { imageOrientation: 'from-image' });
  } catch {
    image = await loadViaImageElement(file);
  }
  const width = image.width ?? image.naturalWidth;
  const height = image.height ?? image.naturalHeight;
  if (!width || !height) throw new Error('unreadable');
  return { image, width, height };
}

async function loadViaImageElement(file) {
  const url = URL.createObjectURL(file);
  try {
    const img = new Image();
    img.src = url;
    await img.decode();
    return img;
  } finally {
    URL.revokeObjectURL(url);
  }
}

// Web Worker 안에는 document가 없어서 OffscreenCanvas를 쓴다.
function makeCanvas(width, height) {
  if (typeof document === 'undefined') return new OffscreenCanvas(width, height);
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  return canvas;
}

function draw(source, width, height, mime) {
  const canvas = makeCanvas(width, height);
  const ctx = canvas.getContext('2d');
  if (mime === 'image/jpeg') {
    // JPG는 투명을 담지 못한다. 그대로 두면 투명한 곳이 검게 나온다.
    ctx.fillStyle = '#fff';
    ctx.fillRect(0, 0, width, height);
  }
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = 'high';
  ctx.drawImage(source.image, 0, 0, width, height);
  return canvas;
}

async function encode(canvas, mime, quality) {
  const blob = canvas.convertToBlob
    ? await canvas.convertToBlob({ type: mime, quality })
    : await new Promise((resolve) => canvas.toBlob(resolve, mime, quality));
  // 지원하지 않는 형식을 요청하면 브라우저가 PNG로 바꿔서 돌려준다.
  if (!blob || blob.type !== mime) throw new Error('unsupported');
  return blob;
}

/**
 * 이 해상도에서 목표 이하가 되는 가장 높은 품질을 찾는다. 못 맞추면 가장 낮은 품질의 결과를 돌려준다.
 * onEncode는 인코딩을 한 번 할 때마다, 이 해상도에서 끝난다면 남은 인코딩 횟수와 함께 불린다.
 */
async function fitQuality(canvas, mime, targetBytes, onEncode) {
  const top = await encode(canvas, mime, MAX_QUALITY);
  if (top.size <= targetBytes) return top;
  onEncode(1 + QUALITY_SEARCH_STEPS);

  const floor = await encode(canvas, mime, MIN_QUALITY);
  if (floor.size > targetBytes) return floor;
  onEncode(QUALITY_SEARCH_STEPS);

  let low = MIN_QUALITY;
  let high = MAX_QUALITY;
  let best = floor;
  for (let i = 0; i < QUALITY_SEARCH_STEPS; i += 1) {
    const mid = (low + high) / 2;
    const blob = await encode(canvas, mime, mid);
    onEncode(QUALITY_SEARCH_STEPS - i - 1);
    if (blob.size <= targetBytes) {
      best = blob;
      low = mid;
    } else {
      high = mid;
    }
  }
  return best;
}

const nextFrame = () => new Promise((resolve) => setTimeout(resolve));

/**
 * @returns {Promise<{blob: Blob, width: number, height: number, resized: boolean, met: boolean}>}
 *   met이 false면 목표에 못 맞춘 것이고, blob은 만들 수 있었던 가장 작은 결과다.
 *   onProgress는 0~1 사이의 어림값을 받는다. 남은 인코딩 횟수를 미리 알 수 없어서 어림이고, 뒤로 가지는 않는다.
 */
export async function compress({ source, format, targetBytes, onStage, onProgress }) {
  const { mime, lossy } = FORMATS[format];
  let scale = Math.min(1, Math.sqrt(MAX_AREA / (source.width * source.height)));
  let smallest = null;

  let encodes = 0;
  let progress = 0;
  const report = (encodesLeft) => {
    encodes += 1;
    progress = Math.max(progress, encodes / (encodes + encodesLeft));
    onProgress?.(progress);
  };

  onStage?.('quality');
  onProgress?.(0);
  for (let step = 0; step < 40; step += 1) {
    const width = Math.max(1, Math.round(source.width * scale));
    const height = Math.max(1, Math.round(source.height * scale));
    const canvas = draw(source, width, height, mime);
    const blob = lossy ? await fitQuality(canvas, mime, targetBytes, report) : await encode(canvas, mime);
    const attempt = { blob, width, height, resized: width !== source.width || height !== source.height };

    if (blob.size <= targetBytes) return { ...attempt, met: true };
    if (!smallest || blob.size < smallest.blob.size) smallest = attempt;
    if (Math.max(width, height) <= MIN_SIDE) break;

    // 한 번에 넓이를 1/4까지만 줄이므로, 목표까지 해상도를 몇 번 더 줄여야 하는지 어림한다.
    const passesLeft = Math.max(1, Math.ceil(Math.log(blob.size / targetBytes) / Math.log(4)));
    report(lossy ? (passesLeft - 1) * 2 + 2 + QUALITY_SEARCH_STEPS : passesLeft);

    onStage?.('resize');
    // 용량은 대략 넓이에 비례하므로, 필요한 배율을 어림잡아 한 번에 10~50%씩 줄인다.
    const estimate = Math.sqrt(targetBytes / blob.size) * 0.97;
    scale *= Math.min(0.9, Math.max(0.5, estimate));
    await nextFrame();
  }
  return { ...smallest, met: false };
}
