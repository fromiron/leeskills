# leeskills

`leeskills`는 디지털 인터페이스, 랜딩 페이지, 포트폴리오, 제품 카피,
디자인 시스템에서 근거 없는 내용과 불필요한 시각 요소를 탐지·제거하기 위한
범용 Agent Skills 모음입니다.

버전: **0.3.0**  
상태: **Beta / 연구 기반 릴리스**  
라이선스: **MIT**

## 핵심 원칙

> 사용자의 핵심 작업, 실제 콘텐츠, 접근성을 보존하면서 가장 적은 수의
> 일관된 시각·언어 문법으로 표현한다.

이 저장소에서 `AI slop`은 범용적이고, 근거가 없거나, 목적 없이 추가된
결과물을 가리키는 운영 용어입니다. 시각적 특징만으로 해당 결과물이 AI로
생성되었다고 단정하지 않습니다.

## 포함된 스킬

| 스킬 | 역할 |
|---|---|
| `anti-ai-slop` | 필요한 집중 스킬을 선택하고 순서를 결정하는 선택형 오케스트레이터 |
| `slop-signal-audit` | 관찰 가능한 slop 신호를 찾고 점수화하며 제거 순서를 제안 |
| `content-grounding` | 출처가 있는 콘텐츠 인벤토리를 만들고 조작·날조를 차단 |
| `structure-selector` | 사용자의 작업에 맞는 지배적 정보 구조 하나를 선택 |
| `visual-entropy-budget` | 시각 변형 수를 제한하고 중첩 Radius 관계를 검증 |
| `specificity-editor` | 교체 가능한 마케팅 문구를 구체적이고 검증 가능한 문구로 수정 |
| `motion-necessity-gate` | 피드백·상태·인과·공간 관계를 전달하는 모션만 유지 |
| `accessibility-simplicity-guard` | 심플화를 이유로 접근성 단서나 기능을 제거하지 못하게 함 |
| `prune-and-verify` | 삭제·치환·리플로·키보드·모션·출처 검증을 수행 |

## 호환 형식

각 스킬은 공개 Agent Skills 디렉터리 형식을 따릅니다.

```text
skill-name/
├── SKILL.md
├── references/
├── assets/
├── scripts/
└── evals/
```

핵심 지침은 특정 벤더에 종속되지 않습니다. 선택형 Python 스크립트는
표준 라이브러리만 사용하며 네트워크 요청을 수행하지 않습니다.

## 설치

공개 [`skills` CLI](https://skills.sh/docs/cli)로 전체 스킬 모음을 설치할 수
있습니다.

```bash
npx skills add fromiron/leeskills
```

CLI는 `skills/` 아래의 스킬 디렉터리를 모두 탐색한 뒤 대상 에이전트와 설치할
스킬을 선택하게 합니다. 설치 전에 목록을 확인하거나 하나만 설치할 수도
있습니다.

```bash
npx skills add fromiron/leeskills --list
npx skills add fromiron/leeskills --skill anti-ai-slop
```

이 저장소 자체를 npm 패키지로 배포할 필요는 없습니다. `npx`가 외부 `skills`
설치기를 실행해 GitHub 저장소의 스킬을 설치합니다.

## 개발

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

예시는 `python` 실행기를 사용합니다. 환경에 따라 Unix 계열에서는
`python3`, Windows에서는 `py -3`로 바꾸어 실행할 수 있습니다.

별도로 clone한 저장소에서 네트워크 없이 설치하려면 포함된 Python 설치기를
사용할 수 있습니다.

```bash
# OpenAI Codex: 현재 저장소 범위
python scripts/install.py --client codex --scope repo --mode copy

# Claude Code: 현재 저장소 범위
python scripts/install.py --client claude-code --scope repo --mode copy

# 기타 Agent Skills 호환 클라이언트
python scripts/install.py --client generic --target /path/to/skills --mode copy
```

먼저 `--dry-run`으로 결과를 확인하십시오. `--force`를 주지 않으면 기존
스킬을 덮어쓰지 않습니다.

Trigger fixture는 영어·한국어·일본어를 모두 포함합니다. 대상 클라이언트에서
각 질의를 실제로 반복 실행한 뒤 `scripts/evaluate_trigger_results.py`로 측정
결과를 평가하십시오. Fixture 커버리지는 실제 trigger rate의 증거가 아닙니다.

## 권장 실행 순서

### 새 인터페이스

```text
content-grounding
→ structure-selector
→ visual-entropy-budget
→ specificity-editor
→ motion-necessity-gate
→ accessibility-simplicity-guard
→ prune-and-verify
```

### 기존 화면 감사

```text
slop-signal-audit
→ content-grounding
→ specificity-editor
→ visual-entropy-budget
→ motion-necessity-gate
→ accessibility-simplicity-guard
→ prune-and-verify
```

### 카피만 검토

```text
content-grounding → specificity-editor → prune-and-verify
```

### 빠른 검토 (소규모 산출물·초안)

```text
slop-signal-audit quick-pass 모드
(1회 실행, 점수·판정 없음, 최대 5개 수정, 생략한 검증 항목 명시)
```

## 근거 상태

모든 판단은 다음 중 하나로 표시합니다.

- **Observed:** 제공된 화면·마크업·카피·토큰에서 직접 확인
- **Measured:** 스크립트나 계산으로 측정
- **Inferred:** 근거를 바탕으로 추론했으며 추론임을 명시
- **Unknown:** 제공 자료로 확인할 수 없음

고객명, 수치, 후기, 수상 경력, 기능, 프로젝트 성과, 접근성 준수 여부를
임의로 만들지 않습니다.

## 점수의 의미

`slop-signal-audit`의 점수는 수정 우선순위를 정하기 위한 보조 수단입니다.
과학적 측정값이나 AI 생성 여부 판별값이 아닙니다. 날조된 증거, 실제처럼
표현된 가짜 제품 UI, 키보드 포커스 제거, 대체 수단 없는 스크롤 강제 등은
총점과 무관하게 통과를 차단합니다.

`unknown` 범주는 해당 범주 최대 점수의 절반까지만 받을 수 있습니다. 프로젝트
하드 실패는 관찰되거나 측정된 근거가 있을 때만 기록합니다.

## 한계

- 스크린샷만으로 접근성 전체 준수를 확인할 수 없습니다.
- 정적 감사만으로 이해도나 전환율을 입증할 수 없습니다.
- 범용 문구 탐지는 오탐이 있으므로 맥락과 근거가 최종 기준입니다.
- 시각 예산은 기본값이며 절대적인 미학 법칙이 아닙니다.
- 스킬 자동 호출은 모델과 클라이언트마다 달라 실제 환경에서 eval이 필요합니다.
