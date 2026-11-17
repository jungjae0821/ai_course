# 사진 용량 줄이기 앱 (Photo Compressor Web App)

## 1. 프로젝트 개요
사용자가 사진의 용량을 원하는 목표치에 맞춰 간편하게 줄일 수 있는 웹 기반 애플리케이션입니다. 서버 업로드 없이 브라우저 내에서 모든 처리가 이루어져 보안과 속도가 빠릅니다.

## 2. 기술 스택
- **Framework**: React
- **Styling**: Tailwind CSS
- **Image Processing**: Client-side Canvas API / browser-image-compression
- **Deployment Target**: Web Browser (Desktop/Mobile)

## 3. 핵심 기능 및 상세 요구사항

### 3.1 사진 선택 및 정보 표시
- **기능**: 기기(휴대폰/PC)에서 이미지 파일을 불러오기.
- **표시 정보**: 
    - 이미지 미리보기
    - 원본 파일 용량 (KB/MB)
    - 이미지 해상도 (가로 $\times$ 세로 크기)

### 3.2 목표 용량 설정
- **Preset 버튼**: 200KB, 500KB, 1MB 등 자주 사용하는 용량 버튼 제공.
- **직접 입력**: 사용자가 원하는 용량 숫자와 단위(KB, MB)를 직접 입력할 수 있는 필드 제공.

### 3.3 스마트 압축 엔진 (Smart Compression)
- **전략**: 화질 저하를 최소화하면서 목표 용량을 달성하는 것을 최우선으로 함.
- **단계별 프로세스**:
    1. **1단계 (Quality Adjustment)**: 이미지의 품질(Quality)을 낮추어 용량을 조절.
    2. **2단계 (Resizing)**: 1단계로 목표 용량에 도달하지 못할 경우, 이미지의 **가로세로 비율(Aspect Ratio)을 유지**하며 해상도를 단계적으로 축소.

### 3.4 결과 확인 및 저장
- **비교 기능**: 압축 전과 후의 용량 차이 및 미리보기를 대조하여 보여줌.
- **저장 규칙**: 압축된 파일은 원본 파일명 뒤에 `_compressed` 접미사를 붙여 저장 (예: `image.jpg` $\rightarrow$ `image_compressed.jpg`).

## 4. UI/UX 가이드라인
- **타겟 사용자**: 일반인 (전문 지식이 없어도 쉽게 사용 가능한 직관적인 인터페이스).
- **디자인 방향**: 깔끔하고 현대적인 UI, Drag & Drop 지원, 모바일 친화적 반응형 레이아웃.
- **스킬 사용**: screendoro 스킬을 사용하여 처음부터 끝까지 진행