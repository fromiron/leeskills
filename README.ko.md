<p align="center">
  <a href="README.md">English</a> · <strong>한국어</strong> · <a href="README.ja.md">日本語</a>
</p>

<h1 align="center">leeskills</h1>

<p align="center">
  <strong>콘텐츠를 근거에 묶고, 소음을 덜어내고, 남은 것을 검증합니다.</strong>
</p>

<p align="center">
  범용적이고 근거 없는 인터페이스 결과물을 더 작고 명확한 근거 기반 시스템으로<br>
  다듬는, 어디서나 쓸 수 있는 Agent Skills 10종입니다.
</p>

<p align="center">
  <a href="https://github.com/fromiron/leeskills/actions/workflows/validate.yml"><img alt="검증 상태" src="https://github.com/fromiron/leeskills/actions/workflows/validate.yml/badge.svg"></a>
  <img alt="버전 0.6.0" src="https://img.shields.io/badge/version-0.6.0-007FA8?style=flat-square">
  <img alt="공개 Agent Skills 형식" src="https://img.shields.io/badge/format-Agent_Skills-111111?style=flat-square">
  <a href="LICENSE"><img alt="MIT 라이선스" src="https://img.shields.io/badge/license-MIT-F4E9D8?style=flat-square"></a>
</p>

## 한 줄로 설치

```bash
npx skills add fromiron/leeskills
```

<p align="center">
  <img src=".github/assets/leeskills-hero.png" width="720" alt="복잡한 인터페이스 조각이 검수 프레임을 지나 명확한 정보 계층으로 정리되는 개념 일러스트">
</p>

<p align="center">개념 일러스트이며, 실제 제품 화면이나 인터페이스의 증거가 아닙니다.</p>

> [!IMPORTANT]
> `leeskills`는 관찰 가능한 디자인 결과물을 감사합니다. AI가 만들었는지
> 판정하지 않으며, 미적 패턴을 제작 주체의 증거로 취급하지 않습니다.

공개 [`skills` CLI](https://skills.sh/docs/cli)는 `skills/` 아래의 패키지를 모두
찾고, 사용할 에이전트와 스킬을 선택하게 합니다. 목록만 보거나
오케스트레이터 하나만 설치할 수도 있습니다.

```bash
npx skills add fromiron/leeskills --list
npx skills add fromiron/leeskills --skill anti-ai-slop
```

이 저장소의 패키지를 npm에 따로 배포할 필요는 없습니다. 위 명령은 외부
설치기로 GitHub 저장소를 가져옵니다.

## leeskills가 다른 점

- **미감보다 근거를 먼저 봅니다.** 주장, 수치, 스크린샷, 성과를 출처에
  연결합니다. 근거가 없으면 모르는 상태로 남깁니다.
- **책임 범위가 분명한 작은 스킬입니다.** 좁은 문제에는 집중 스킬 하나를
  쓰고, 넓은 문제에는 `anti-ai-slop`이 필요한 최소 순서를 고릅니다.
- **판단은 에이전트가, 기계적 검사는 스크립트가 맡습니다.** 맥락이 필요한
  디자인 판단은 에이전트가 하고, 스키마와 외부 의존성 없는 Python 도구는
  기계적인 계약을 검사합니다.
- **처음부터 이식 가능합니다.** 핵심 스킬은 벤더 전용 frontmatter 대신 공개
  Agent Skills 형식을 씁니다. Codex, Claude Code, 범용 호환 클라이언트용
  어댑터가 포함됩니다.

## 10개 스킬, 하나의 근거 계약

| 필요한 일 | 스킬 | 결과물 |
|---|---|---|
| 전체 흐름을 아우르는 검토 | `anti-ai-slop` | 적용할 최소 워크플로와 통합 판정 |
| 기존 결과물 진단 | `slop-signal-audit` | 관찰 가능한 발견 사항, 위험 점수, 제거 우선순위 |
| 사실 기반 마련 | `content-grounding` | 출처를 추적한 콘텐츠 인벤토리와 날조 차단 |
| 지배적 정보 구조 하나 선택 | `structure-selector` | 탈락 대안까지 기록한 작업 기반 구조 결정 |
| 재사용 UI 계약 정의 | `component-contract-audit` | Anatomy, 상태, 동작, 접근성, 소유권, parity 검사 |
| 일관된 시각 시스템 정리 | `visual-entropy-budget` | 시각 예산과 반응형·타이포그래피·중첩 radius 검사 |
| 제품다운 구체적 카피 작성 | `specificity-editor` | 치환 테스트를 견디는 근거 기반 문구 |
| 필요한 모션만 유지 | `motion-necessity-gate` | 유지·축소·대체·제거 결정과 reduced-motion 검사 |
| 접근성을 잃지 않는 단순화 | `accessibility-simplicity-guard` | 시맨틱·키보드·포커스·리플로·대비·상태 보호 |
| 최종 결과 검증 | `prune-and-verify` | 삭제·확장·리플로·출처·핵심 작업 검증 |

이 스킬들은 카드, 그라디언트, 모션, 표현적인 작업을 종류만 보고 금지하지
않습니다. 각 선택이 무엇을 전달하고, 어떤 작업을 돕고, 무엇을 근거로 남아야
하는지 묻습니다.

## 가장 작은 워크플로를 고르세요

**새 인터페이스·랜딩 페이지**

```text
content-grounding
→ structure-selector
→ visual-entropy-budget
→ specificity-editor
→ motion-necessity-gate
→ accessibility-simplicity-guard
→ prune-and-verify
```

**기존 인터페이스 감사**

```text
slop-signal-audit
→ 필요한 집중 스킬
→ prune-and-verify
```

**디자인 시스템·재사용 컴포넌트**

```text
component-contract-audit
→ visual-entropy-budget
→ accessibility-simplicity-guard
→ prune-and-verify
```

**카피만 검토**

```text
content-grounding → specificity-editor → prune-and-verify
```

작은 결과물이나 초기 초안에는 `slop-signal-audit`의 quick-pass 모드를
사용하세요. 한 번만 실행하고, 점수나 판정 없이 최대 5개 수정과 생략한 검사를
명시합니다.

## 느낌 대신 근거

중요한 판단마다 근거 상태 하나를 유지합니다.

| 상태 | 의미 |
|---|---|
| **Observed** | 제공된 카피·스크린샷·마크업·코드·디자인 파일·토큰에서 직접 확인 |
| **Measured** | 결정론적 테스트나 계산으로 측정 |
| **Inferred** | 확보한 근거에서 추론했으며 추론임을 명시 |
| **Unknown** | 제공 자료로는 확인할 수 없음 |

추론은 반복해서 말해도 사실이 되지 않습니다. 고객명, 수치, 후기, 수상 경력,
기능, 성과, 접근성 준수 여부를 만들어내는 행위를 금지합니다. 구조화된 검증기도
필수 항목의 `unknown`을 몰래 통과로 바꾸지 않습니다.

## 이식 가능한 패키지, 결정론적 검사

```text
skill-name/
├── SKILL.md      # 핵심 워크플로
├── references/   # 필요할 때만 읽는 참고 자료
├── assets/       # 스키마와 템플릿
├── scripts/      # 선택형 결정론적 도구
└── evals/        # 트리거·출력 품질 fixture
```

- 핵심 지침은 공개 Agent Skills 필드만 사용하며 특정 벤더에 종속되지 않습니다.
- 선택형 Python 3.9+ 스크립트는 비대화형이며, 표준 라이브러리만 사용하고,
  네트워크 요청을 하지 않습니다.
- 트리거 fixture는 영어·한국어·일본어와 near-miss negative를 포함합니다.
  Fixture는 범위를 증명할 뿐 실제 클라이언트의 trigger rate를 증명하지 않습니다.
- JSON 스키마는 구조가 도움이 되는 handoff를 검토 가능하게 만듭니다. 정보 계층,
  진정성, 목소리, 사용성은 여전히 사람이 판단해야 합니다.

## 실제 작업에 써보기

설치 후 평소 말하듯 에이전트에게 요청하세요.

> 이 랜딩 페이지에서 범용적이거나, 근거가 없거나, 불필요한 디자인을 감사해줘.
> 실제 정체성, 필요한 행동, 접근성은 보존하고 모든 판단에 근거 상태를 표시해.
> 가장 작은 완전한 수정을 한 뒤 핵심 흐름을 다시 검증해줘.

[전체 감사 요청 예시](examples/full-audit-request.md),
[수동 통합 예시](examples/manual-agent-integration.md), 또는
[`examples/`의 구조화된 결과물](examples/README.md)에서 시작할 수 있습니다.

## 개발·검증

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

사용 가능한 Python 3.9+ 실행기에 따라 Unix 계열에서는 `python3`, Windows에서는
`py -3`를 사용해도 됩니다. CI는 Ubuntu와 Windows, Python 3.9와 3.12에서 같은
검사를 실행합니다.

오프라인 clone이나 명시한 경로에 설치할 때는 포함된 설치기를 사용하세요.

```bash
python scripts/install.py --client codex --scope repo --mode copy --dry-run
python scripts/install.py --client claude-code --scope repo --mode copy --dry-run
python scripts/install.py --client generic --target /path/to/skills --mode copy --dry-run
```

`--force`를 주지 않으면 기존 스킬을 덮어쓰지 않습니다.

## 다음 문서

| 문서 | 다루는 내용 |
|---|---|
| [아키텍처](docs/architecture.md) | 구성, 데이터 계약, 이식성 경계 |
| [통합](docs/integration.md) | 클라이언트 설정과 호출 전략 |
| [평가](docs/evaluation.md) | 트리거 측정, 출력 비교, 릴리스 기준 |
| [디자인 기초](docs/design-foundations.md) | 정규화한 제품·디자인 원칙 |
| [출처 노트](docs/source-notes.md) | 근거와 외부 지침을 적용하는 한계 |
| [기여 안내](CONTRIBUTING.md) | 저장소 규칙과 기여 흐름 |

## 솔직한 한계

- 스크린샷만으로 런타임 동작이나 접근성 전체 준수를 확인할 수 없습니다.
- 정적 감사만으로 이해도나 전환율을 입증할 수 없습니다.
- 문구·패턴 lint에는 오탐이 있으므로 맥락이 최종 기준입니다.
- 시각 예산은 기본값이지 절대적인 미학 법칙이 아닙니다.
- 스킬 호출은 비결정적이므로 trigger rate를 보고하기 전에 대상 클라이언트에서
  실제로 측정해야 합니다.

## 라이선스

[MIT](LICENSE). 자유롭게 사용하고 수정하되 근거의 경계는 지켜주세요.
