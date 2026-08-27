<p align="center">
  <a href="README.md">English</a> · <strong>한국어</strong> · <a href="README.ja.md">日本語</a>
</p>

<h1 align="center">leeskills</h1>

<p align="center">
  <strong>인터페이스에서 근거 없는 카피, 필요 없는 장식, 일관되지 않은 동작을 찾아내는 Agent Skills.</strong>
</p>

<p align="center">
  콘텐츠, 정보 구조, 컴포넌트, 시각 체계, 모션, 접근성, 최종 검증을<br>
  10개 스킬로 나눴습니다.
</p>

<p align="center">
  <a href="https://github.com/fromiron/leeskills/actions/workflows/validate.yml"><img alt="검증 상태" src="https://github.com/fromiron/leeskills/actions/workflows/validate.yml/badge.svg"></a>
  <img alt="버전 0.6.0" src="https://img.shields.io/badge/version-0.6.0-007FA8?style=flat-square">
  <img alt="공개 Agent Skills 형식" src="https://img.shields.io/badge/format-Agent_Skills-111111?style=flat-square">
  <a href="LICENSE"><img alt="MIT 라이선스" src="https://img.shields.io/badge/license-MIT-F4E9D8?style=flat-square"></a>
</p>

## 설치

```bash
npx skills add fromiron/leeskills
```

<p align="center">
  <img src=".github/assets/leeskills-hero.png" width="720" alt="복잡한 인터페이스 조각이 검토 프레임을 지나 명확한 정보 구조로 정리되는 그림">
</p>

<p align="center">검토 과정을 표현한 그림입니다. 실제 제품 화면은 아닙니다.</p>

`leeskills`는 눈앞의 결과물만 봅니다. 누가 어떤 도구로 만들었는지는 추측하지
않습니다.

공개 [`skills` CLI](https://skills.sh/docs/cli)가 `skills/` 디렉터리의 패키지를
찾아 설치합니다. 먼저 목록을 보거나 `anti-ai-slop`만 골라 설치할 수도 있습니다.

```bash
npx skills add fromiron/leeskills --list
npx skills add fromiron/leeskills --skill anti-ai-slop
```

설치기는 이 GitHub 저장소를 가져옵니다. npm에 따로 배포할 필요는 없습니다.

## 쓰는 법

검토할 범위가 좁다면 맞는 스킬 하나만 쓰면 됩니다. 화면 전체를 살필 때는
`anti-ai-slop`으로 시작하세요. 결과물에 필요한 검사만 골라서 연결합니다.

스킬 문서는 에이전트가 판단할 기준을 담고 있습니다. 파일 구조나 필수 필드처럼
반복해서 확인할 수 있는 항목은 스키마와 외부 의존성이 없는 Python 스크립트가
검사합니다.

## 들어 있는 스킬

| 할 일 | 스킬 | 결과 |
|---|---|---|
| 전체 인터페이스 검토 | `anti-ai-slop` | 필요한 스킬 순서와 전체 결과 |
| 기존 결과물 진단 | `slop-signal-audit` | 확인한 문제, 위험 점수, 고칠 순서 |
| 카피의 사실 확인 | `content-grounding` | 출처가 붙은 콘텐츠 목록과 확인할 수 없는 항목 |
| 정보 구조 선택 | `structure-selector` | 사용자 작업을 기준으로 고른 구조와 제외한 대안 |
| 재사용 UI 규칙 정리 | `component-contract-audit` | 구조, 상태, 동작, 접근성, 담당 범위, 디자인과 코드의 차이 |
| 시각 체계 정리 | `visual-entropy-budget` | 시각 규칙과 반응형·타이포그래피·중첩된 모서리 반경 검사 |
| 모호한 카피 수정 | `specificity-editor` | 제공된 사실에 맞춰 구체적으로 고친 문구 |
| 모션 검토 | `motion-necessity-gate` | 유지·축소·대체·삭제 판단과 모션 감소 검사 |
| 접근성을 지키며 단순화 | `accessibility-simplicity-guard` | 문서 구조, 키보드, 포커스, 리플로, 대비, 상태 검사 |
| 수정한 결과 확인 | `prune-and-verify` | 삭제, 확장, 리플로, 출처, 핵심 작업 검사 |

카드나 그라디언트, 모션 자체를 금지하지는 않습니다. 사용자 작업에 도움이 되고
남길 이유가 있으면 그대로 둡니다.

## 자주 쓰는 순서

**새 인터페이스나 랜딩 페이지**

```text
content-grounding
→ structure-selector
→ visual-entropy-budget
→ specificity-editor
→ motion-necessity-gate
→ accessibility-simplicity-guard
→ prune-and-verify
```

**기존 인터페이스 검토**

```text
slop-signal-audit
→ 필요한 집중 스킬
→ prune-and-verify
```

**디자인 시스템이나 재사용 컴포넌트**

```text
component-contract-audit
→ visual-entropy-budget
→ accessibility-simplicity-guard
→ prune-and-verify
```

**카피 검토**

```text
content-grounding → specificity-editor → prune-and-verify
```

작은 초안은 `slop-signal-audit`의 `quick-pass`로 빠르게 훑어볼 수 있습니다.
점수나 출시 판정 없이 중요한 수정만 다섯 개 이하로 추리고, 확인하지 못한 항목도
함께 적습니다.

## 근거 표시

검토 결과에는 다음 네 가지 중 하나를 붙입니다.

| 표시 | 뜻 |
|---|---|
| **Observed** | 제공된 문구, 화면, 코드, 디자인 파일, 토큰에서 바로 확인한 내용 |
| **Measured** | 테스트나 계산으로 나온 값 |
| **Inferred** | 근거를 바탕으로 판단했지만 직접 확인하지 못한 내용 |
| **Unknown** | 제공된 자료만으로는 알 수 없는 내용 |

확인할 수 없는 내용은 그럴듯한 고객명이나 수치, 후기, 기능, 성과로 채우지
않습니다.

## 패키지 구조

```text
skill-name/
├── SKILL.md      # 스킬 지침
├── references/   # 필요할 때 읽는 자료
├── assets/       # 스키마와 템플릿
├── scripts/      # 반복 검사용 도구
└── evals/        # 트리거·출력 평가 항목
```

- 핵심 지침은 공개 Agent Skills 필드만 쓰며 벤더 전용 frontmatter를 넣지 않습니다.
- 선택형 Python 3.9+ 스크립트는 표준 라이브러리만 사용하고, 비대화형으로
  실행되며, 네트워크에 연결하지 않습니다.
- 평가 항목은 영어·한국어·일본어 예시와, 비슷해 보여도 호출되면 안 되는 예시를
  함께 담습니다. 평가 파일만으로 실제 클라이언트의 호출률을 알 수는 없습니다.
- Codex, Claude Code, 그 밖의 호환 클라이언트용 어댑터가 들어 있습니다.

## 요청 예시

설치한 뒤 평소 말하듯 요청하면 됩니다.

> 이 랜딩 페이지를 leeskills로 검토해 줘. 근거 없는 카피와 필요 없는 디자인을
> 찾되, 제품의 말투와 중요한 기능, 접근성은 그대로 둬. 직접 확인한 내용과
> 추정한 내용을 구분하고, 꼭 필요한 만큼만 고친 뒤 핵심 흐름을 다시 확인해 줘.

[전체 검토 요청](examples/full-audit-request.md),
[수동 통합 예시](examples/manual-agent-integration.md),
[`examples/` 디렉터리](examples/README.md)에도 예시가 있습니다.

## 개발과 테스트

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

사용할 수 있는 Python 3.9+ 실행기에 따라 Unix 계열에서는 `python3`, Windows에서는
`py -3`을 써도 됩니다. CI는 Ubuntu와 Windows에서 Python 3.9와 3.12로 같은 검사를
실행합니다.

오프라인 복제본이나 원하는 경로에 설치할 때는 저장소에 포함된 설치기를 씁니다.

```bash
python scripts/install.py --client codex --scope repo --mode copy --dry-run
python scripts/install.py --client claude-code --scope repo --mode copy --dry-run
python scripts/install.py --client generic --target /path/to/skills --mode copy --dry-run
```

`--force`를 붙이지 않으면 기존 스킬을 덮어쓰지 않습니다.

## 문서

| 문서 | 내용 |
|---|---|
| [아키텍처](docs/architecture.md) | 구성, 데이터 계약, 이식 범위 |
| [통합](docs/integration.md) | 클라이언트 설정과 호출 방식 |
| [평가](docs/evaluation.md) | 호출 측정, 결과 비교, 릴리스 기준 |
| [디자인 기초](docs/design-foundations.md) | 스킬이 따르는 제품·디자인 원칙 |
| [출처 노트](docs/source-notes.md) | 출처와 외부 지침을 다루는 방식 |
| [기여 안내](CONTRIBUTING.md) | 저장소 규칙과 기여 절차 |

## 라이선스

[MIT](LICENSE)
