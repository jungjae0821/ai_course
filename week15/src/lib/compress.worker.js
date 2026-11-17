import { compress } from './compress.js';

self.onmessage = async ({ data }) => {
  const { image, width, height, format, targetBytes } = data;
  try {
    const result = await compress({
      source: { image, width, height },
      format,
      targetBytes,
      onStage: (stage) => self.postMessage({ type: 'stage', stage }),
      onProgress: (progress) => self.postMessage({ type: 'progress', progress }),
    });
    self.postMessage({ type: 'done', result });
  } catch (error) {
    self.postMessage({ type: 'error', message: error.message });
  } finally {
    // 넘겨받은 사진은 복사본이라 여기서 닫아야 메모리가 풀린다.
    image.close();
  }
};
