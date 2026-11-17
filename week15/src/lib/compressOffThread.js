// 압축을 Web Worker에서 돌려서, 큰 사진을 줄이는 동안에도 화면이 멈추지 않게 한다.
// Worker를 쓸 수 없는 브라우저나 사진이면 화면 스레드에서 그대로 돌린다.

import { compress } from './compress.js';

const workerReady =
  typeof Worker !== 'undefined' && typeof OffscreenCanvas !== 'undefined' && typeof ImageBitmap !== 'undefined';

function runInWorker({ source, format, targetBytes, onStage, onProgress }) {
  return new Promise((resolve, reject) => {
    const worker = new Worker(new URL('./compress.worker.js', import.meta.url), { type: 'module' });
    const finish = (settle, value) => {
      worker.terminate();
      settle(value);
    };
    worker.onmessage = ({ data }) => {
      if (data.type === 'stage') onStage?.(data.stage);
      else if (data.type === 'progress') onProgress?.(data.progress);
      else if (data.type === 'done') finish(resolve, data.result);
      else finish(reject, new Error(data.message));
    };
    worker.onerror = (event) => {
      event.preventDefault();
      finish(reject, new Error('worker'));
    };
    worker.postMessage({ image: source.image, width: source.width, height: source.height, format, targetBytes });
  });
}

/** compress와 같은 값을 받고 같은 값을 돌려준다. */
export async function compressOffThread(options) {
  // createImageBitmap이 실패해 <img>로 연 사진은 Worker로 보낼 수 없다.
  if (!workerReady || !(options.source.image instanceof ImageBitmap)) return compress(options);
  try {
    return await runInWorker(options);
  } catch (error) {
    // 'unsupported'는 형식 문제라 어디서 돌려도 같다. 그 밖의 실패는 Worker 쪽 문제일 수 있어 한 번 더 해 본다.
    if (error.message === 'unsupported') throw error;
    return compress(options);
  }
}
