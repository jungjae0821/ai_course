import { useEffect, useRef, useState } from 'react';
import { FORMATS, compress, formatBytes, formatOf, loadSource, outputName } from './lib/compress.js';

const UNITS = { KB: 1024, MB: 1024 * 1024 };

const STAGE_TEXT = {
  quality: '화질을 조절하고 있어요.',
  resize: '화질만으로는 모자라서 사진 크기를 줄이고 있어요.',
};

const button =
  'font-title font-bold rounded-btn min-h-12 px-6 transition-[background-color,scale] duration-150 active:scale-[0.98]';
const buttonInk = `${button} bg-ink text-print hover:bg-ink-soft`;
const buttonPrint = `${button} bg-print text-ink hover:bg-paper-deep`;
const buttonQuiet = `${button} bg-paper-deep text-ink hover:bg-rule`;
const field = 'bg-print text-ink rounded-field min-h-12 px-3';

function saveFile(url, name) {
  const link = document.createElement('a');
  link.href = url;
  link.download = name;
  document.body.append(link);
  link.click();
  link.remove();
}

function Print({ src, alt, width, height, children }) {
  return (
    <figure className="bg-print rounded-print shadow-print p-2.5 pb-3">
      <img
        src={src}
        alt={alt}
        width={width}
        height={height}
        className="block h-auto max-h-[min(20rem,40vh)] w-full object-contain"
      />
      {children}
    </figure>
  );
}

export default function App() {
  const [photo, setPhoto] = useState(null);
  const [amount, setAmount] = useState('');
  const [unit, setUnit] = useState('KB');
  const [ext, setExt] = useState('jpg');
  const [working, setWorking] = useState(false);
  const [stage, setStage] = useState('quality');
  const [result, setResult] = useState(null);
  const [formError, setFormError] = useState('');
  const [openError, setOpenError] = useState('');
  const [dragging, setDragging] = useState(false);

  const picker = useRef(null);
  const amountInput = useRef(null);
  const dragDepth = useRef(0);
  const urls = useRef({ photo: null, result: null });
  const savedNotice = useRef(null);

  // 결과는 설정 표보다 위에 생기므로, 저장 알림이 보이도록 올려 준다.
  useEffect(() => {
    if (!result) return;
    const calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    savedNotice.current?.scrollIntoView({ block: 'nearest', behavior: calm ? 'auto' : 'smooth' });
  }, [result]);

  useEffect(() => {
    const held = urls.current;
    return () => {
      if (held.photo) URL.revokeObjectURL(held.photo);
      if (held.result) URL.revokeObjectURL(held.result);
    };
  }, []);

  async function openPhoto(file) {
    if (!file || working) return;
    if (!file.type.startsWith('image/')) {
      setOpenError('사진 파일만 올릴 수 있어요.');
      return;
    }
    let source;
    try {
      source = await loadSource(file);
    } catch {
      setOpenError('이 사진은 열 수 없어요. JPG, PNG, WebP 사진을 골라 주세요.');
      return;
    }
    if (urls.current.photo) URL.revokeObjectURL(urls.current.photo);
    if (urls.current.result) URL.revokeObjectURL(urls.current.result);
    urls.current = { photo: URL.createObjectURL(file), result: null };

    const format = formatOf(file);
    setPhoto({ file, source, format, url: urls.current.photo });
    setExt(format.key ?? 'jpg');
    setAmount('');
    setResult(null);
    setFormError('');
    setOpenError('');
    if (window.matchMedia('(pointer: fine)').matches) {
      requestAnimationFrame(() => amountInput.current?.focus());
    }
  }

  async function shrink(event) {
    event.preventDefault();
    if (working) return;

    const value = Number(amount.trim().replace(',', '.'));
    if (!amount.trim() || !Number.isFinite(value) || value <= 0) {
      setFormError('목표 용량을 숫자로 적어 주세요.');
      amountInput.current?.focus();
      return;
    }
    const targetBytes = Math.floor(value * UNITS[unit]);
    if (targetBytes >= photo.file.size) {
      setFormError(`목표 용량은 기존 용량(${formatBytes(photo.file.size)})보다 작아야 해요.`);
      amountInput.current?.focus();
      return;
    }

    setFormError('');
    setStage('quality');
    setWorking(true);
    try {
      const output = await compress({ source: photo.source, format: ext, targetBytes, onStage: setStage });
      const name = outputName(photo.file.name, ext);
      if (urls.current.result) URL.revokeObjectURL(urls.current.result);
      urls.current.result = URL.createObjectURL(output.blob);
      setResult({
        url: urls.current.result,
        name,
        size: output.blob.size,
        width: output.width,
        height: output.height,
        resized: output.resized,
        met: output.met,
        target: `${amount.trim()}${unit}`,
      });
      saveFile(urls.current.result, name);
    } catch (error) {
      setFormError(
        error.message === 'unsupported'
          ? `이 브라우저에서는 ${FORMATS[ext].label}로 저장할 수 없어요. 다른 확장자를 골라 주세요.`
          : '사진을 줄이지 못했어요. 다시 눌러 주세요.',
      );
    } finally {
      setWorking(false);
    }
  }

  const dropHandlers = {
    onDragEnter: (event) => {
      event.preventDefault();
      dragDepth.current += 1;
      setDragging(true);
    },
    onDragOver: (event) => event.preventDefault(),
    onDragLeave: () => {
      dragDepth.current -= 1;
      if (dragDepth.current <= 0) setDragging(false);
    },
    onDrop: (event) => {
      event.preventDefault();
      dragDepth.current = 0;
      setDragging(false);
      openPhoto(event.dataTransfer.files[0]);
    },
  };

  const choosePhoto = () => picker.current?.click();
  // 반올림 때문에 "100% 줄었어요"가 나오지 않게 99에서 멈춘다.
  const saved = result ? Math.min(99, Math.round((1 - result.size / photo.file.size) * 100)) : 0;

  return (
    <div
      className={`min-h-dvh transition-colors duration-150 ${dragging && photo ? 'bg-paper-deep' : ''}`}
      {...dropHandlers}
    >
      <header className="mx-auto max-w-[520px] px-5 pt-[clamp(28px,6vw,64px)] pb-7 text-center">
        <h1 className="font-title text-[clamp(1.7rem,5vw,2.3rem)] leading-tight font-bold">사진 용량 줄이기</h1>
        <p className="mt-1.5 text-ink-soft">로그인 없이, 원하는 용량으로 바로 줄여요.</p>
      </header>

      <main className="mx-auto max-w-[520px] px-5 pb-14">

        <input
          ref={picker}
          type="file"
          accept="image/*"
          className="sr-only"
          tabIndex={-1}
          aria-hidden="true"
          onChange={(event) => {
            openPhoto(event.target.files[0]);
            event.target.value = '';
          }}
        />

        {!photo && (
          <>
            <div
              onClick={choosePhoto}
              className={`flex min-h-[52vh] cursor-pointer flex-col items-center justify-center gap-[18px] rounded-drop px-5 py-8 text-center shadow-print transition-colors duration-150 ${dragging ? 'bg-paper-deep' : 'bg-print'}`}
            >
              <strong className="font-title text-[clamp(1.4rem,4.4vw,1.9rem)] leading-snug font-bold">
                {dragging ? (
                  '여기에 놓으세요'
                ) : (
                  <>
                    <span className="pointer-coarse:hidden">
                      사진을 여기에
                      <br />
                      끌어다 놓으세요
                    </span>
                    <span className="hidden pointer-coarse:inline">
                      줄일 사진을
                      <br />
                      골라 주세요
                    </span>
                  </>
                )}
              </strong>
              <button
                type="button"
                className={buttonInk}
                onClick={(event) => {
                  event.stopPropagation();
                  choosePhoto();
                }}
              >
                사진 고르기
              </button>
            </div>
            <p className="mt-4 text-center text-[0.95rem] text-ink-soft">
              사진은 이 기기 안에서만 처리되고, 어디에도 올라가지 않아요.
            </p>
          </>
        )}

        {photo && (
          <>
            {result && (
              <div ref={savedNotice} role="status" className="mb-4 scroll-mt-4 rounded-btn bg-ink px-4 py-3.5 text-print">
                <strong className="block font-title font-bold">저장했어요</strong>
                <span className="block text-[0.9rem] break-all tabular-nums">{result.name}</span>
              </div>
            )}

            {result ? (
              <div key={result.url} className="grid animate-settle grid-cols-2 gap-3">
                <Print src={photo.url} alt="기존 사진" width={photo.source.width} height={photo.source.height}>
                  <figcaption className="mt-2.5 text-center text-[0.9rem]">
                    기존
                    <b className="block font-title text-[1.1rem] font-bold tabular-nums">
                      {formatBytes(photo.file.size)}
                    </b>
                    <span className="tabular-nums">
                      {photo.source.width} × {photo.source.height}
                    </span>
                  </figcaption>
                </Print>
                <Print src={result.url} alt="줄인 사진" width={result.width} height={result.height}>
                  <figcaption className="mt-2.5 text-center text-[0.9rem]">
                    줄인 사진
                    <b className="block font-title text-[1.1rem] font-bold tabular-nums">{formatBytes(result.size)}</b>
                    <span className="tabular-nums">
                      {result.width} × {result.height}
                    </span>
                    {!result.resized && ' (그대로)'}
                  </figcaption>
                </Print>
              </div>
            ) : (
              <Print
                src={photo.url}
                alt="올린 사진 미리보기"
                width={photo.source.width}
                height={photo.source.height}
              />
            )}

            {result && (
              <p className="mt-3.5 text-center font-title text-2xl font-bold tabular-nums">{saved}% 줄었어요</p>
            )}

            {result && !result.met && (
              <p className="mt-3 rounded-btn bg-warn-bg px-4 py-3 text-warn">
                목표 {result.target}에는 맞추지 못했어요. 가장 작게 줄인 {formatBytes(result.size)}로 저장했어요.
              </p>
            )}

            <div className="mt-3 flex flex-wrap justify-center gap-2">
              {result && (
                <button type="button" className={buttonPrint} onClick={() => saveFile(result.url, result.name)}>
                  다시 저장
                </button>
              )}
              <button type="button" className={buttonQuiet} onClick={choosePhoto}>
                다른 사진 고르기
              </button>
            </div>

            <form onSubmit={shrink} noValidate>
              <table className="mt-[18px] w-full border-collapse">
                <thead>
                  <tr className="text-left font-title text-[0.85rem] font-medium text-ink-soft">
                    <th scope="col" className="px-1.5 pb-2">
                      <span className="sr-only">항목</span>
                    </th>
                    <th scope="col" className="px-1.5 pb-2 font-medium">
                      기존
                    </th>
                    <th scope="col" className="px-1.5 pb-2 font-medium">
                      바꿀 값
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-t border-rule">
                    <th scope="row" className="w-[4.2em] px-1.5 py-3.5 text-left font-title text-[0.95rem] font-bold">
                      용량
                    </th>
                    <td className="w-[7.5em] px-1.5 py-3.5 font-title font-medium tabular-nums">
                      {formatBytes(photo.file.size)}
                    </td>
                    <td className="px-1.5 py-3.5">
                      <div className="flex gap-1.5">
                        <input
                          ref={amountInput}
                          value={amount}
                          onChange={(event) => setAmount(event.target.value)}
                          inputMode="decimal"
                          autoComplete="off"
                          placeholder="예: 500"
                          aria-label="목표 용량"
                          aria-invalid={formError ? 'true' : undefined}
                          aria-describedby="form-message"
                          className={`${field} w-full min-w-0 font-title text-[1.15rem] font-medium tabular-nums`}
                        />
                        <select
                          value={unit}
                          onChange={(event) => setUnit(event.target.value)}
                          aria-label="용량 단위"
                          className={field}
                        >
                          <option>KB</option>
                          <option>MB</option>
                        </select>
                      </div>
                    </td>
                  </tr>
                  <tr className="border-t border-rule">
                    <th scope="row" className="px-1.5 py-3.5 text-left font-title text-[0.95rem] font-bold">
                      해상도
                    </th>
                    <td className="px-1.5 py-3.5 font-title font-medium tabular-nums">
                      {photo.source.width} × {photo.source.height}
                    </td>
                    <td className="px-1.5 py-3.5 text-[0.85rem] text-ink-soft">
                      {result?.resized
                        ? `${result.width} × ${result.height}로 줄였어요`
                        : '꼭 필요할 때만 줄여요'}
                    </td>
                  </tr>
                  <tr className="border-t border-rule">
                    <th scope="row" className="px-1.5 py-3.5 text-left font-title text-[0.95rem] font-bold">
                      확장자
                    </th>
                    <td className="px-1.5 py-3.5 font-title font-medium">{photo.format.label}</td>
                    <td className="px-1.5 py-3.5">
                      <select
                        value={ext}
                        onChange={(event) => setExt(event.target.value)}
                        aria-label="바꿀 확장자"
                        className={`${field} w-full`}
                      >
                        {Object.entries(FORMATS).map(([key, format]) => (
                          <option key={key} value={key}>
                            {format.label}
                            {key === photo.format.key ? ' (그대로)' : ''}
                          </option>
                        ))}
                      </select>
                    </td>
                  </tr>
                </tbody>
              </table>

              <p id="form-message" role="alert" className="mt-1 font-title font-medium text-stamp empty:hidden">
                {formError}
              </p>

              <button type="submit" aria-disabled={working} className={`${buttonInk} mt-5 min-h-14 w-full ${working ? 'cursor-progress bg-ink-soft' : ''}`}>
                {working ? '줄이는 중…' : '줄이기'}
              </button>
              <p aria-live="polite" className="mt-2 text-center text-[0.95rem] text-ink-soft empty:hidden">
                {working ? STAGE_TEXT[stage] : ''}
              </p>
            </form>
          </>
        )}

        <p role="alert" className="mt-4 text-center font-title font-medium text-stamp empty:hidden">
          {openError}
        </p>
      </main>
    </div>
  );
}
