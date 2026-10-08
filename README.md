# love-agent

<div align="center">

**AI Relationship Advisor + Chat Intelligence Skill**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-24%2F24_passing-brightgreen.svg)](tests/)
[![GitHub](https://img.shields.io/github/stars/wumumofashi/love-agent?style=social)](https://github.com/wumumofashi/love-agent)

[English](#english) · [中文](#中文) · [日本語](#日本語) · [한국어](#한국어) · [Español](#español) · [Français](#français) · [Deutsch](#deutsch) · [Tiếng Việt](#tiếng-việt) · [Indonesia](#indonesian) · [ภาษาไทย](#thai)

</div>

---

## English

### What is love-agent?

A closed-loop AI relationship advisor that analyzes chat messages, predicts response outcomes, and generates context-aware reply suggestions. Built for serious daters who want strategic, evidence-based communication advice—not generic pickup lines.

### Core Pipeline (10-step chain)

```
Observe → Remember → Interpret → Estimate → Strategize → Generate → Simulate → Critique → Revise → Decide → Send → Update Memory
```

Each step has a dedicated LLM prompt. The system uses **evidence-based reasoning** (confidence scores, source citations) rather than assumptions.

### Key Features

| Feature | Description |
|---------|-------------|
| 🧠 **Relationship Stage Detection** | Classifies relationship phase: stranger → acquaintance → flirting → dating → conflict → breakup → reconciliation |
| 💬 **Context-Aware Replies** | Generates replies matching your persona and the other person's personality |
| 🔮 **Response Simulation** | Simulates how they might react to each suggested reply |
| 🛡️ **Critic & Revise Loop** | 12-point safety check; auto-revises unsafe or tone-deaf replies |
| 📝 **Long-term Memory** | Per-person card system with tagged insights (work, location, hobbies, values...) |
| 🏷️ **Auto-Tag Extraction** | Automatically extracts and stores key facts from conversations |
| 📱 **Multi-modal Input** | Supports text, images (OCR), voice (transcription), screenshots |
| ⚙️ **Three Modes** | `suggest` (read-only) / `confirm` (review before send) / `autopilot` (auto-send when confidence ≥ 0.85) |

### Quick Start

```bash
# Install
pip install -r requirements.txt

# Run tests
python tests/run_tests.py

# Analyze a message
python bin/love_agent.py --content "Hey, long time no talk" --mode suggest

# With full context
python bin/love_agent.py --json '{
  "content": "Message here",
  "person": {"user_age": "26", "other_age": "24", ...},
  "mode": "confirm"
}'
```

### Project Structure

```
love-agent/
├── bin/love_agent.py          # CLI entry point
├── love_agent/
│   ├── engine.py              # Main pipeline engine
│   └── memory.py              # Person card + insights storage
├── llm/prompts/               # 7 LLM prompt templates
├── reply/                     # planner/generator/simulator/critic
├── knowledge/                 # Tiered knowledge base
├── brain/                     # Psychology frameworks
├── memory/people/             # Per-person card files
│   └── person_001/
│       ├── profile.json       # Basic info + context
│       ├── insights.json      # Auto-tagged facts
│       ├── relationship.json  # Stage tracking
│       └── ...
├── config/                    # Model config + defaults
├── tests/                     # 24 scenario tests
└── SKILL.md                   # Agent integration spec
```

### Multi-Person Card System

Each relationship gets its own card. Switch between people without mixing memories:

```python
# person_001 = 二妹
# person_002 = next crush
# Each has isolated profile, insights, conversation history
```

### Auto-Tag Categories

When analyzing messages, the system automatically extracts and stores:
- **work** — profession, company, career level
- **income** — salary range, financial situation
- **location** — city, country, living situation
- **hobbies** — interests, activities, preferences
- **education** — school, degree, academic background
- **family** — parents, siblings, relationship with family
- **relationship_history** — past relationships, breakups
- **personality_detail** — temperament, emotional patterns
- **lifestyle** — daily routine, habits, health
- **values** — life philosophy, priorities, beliefs
- **speech_style** — communication patterns, humor style
- **taboo_topics** — sensitive subjects, boundaries
- **dating_preference** — what they look for in a partner
- **social_circle** — friends, social habits
- **future_plans** — goals, timeline, ambitions
- **+ 4 more categories**

### Safety & Ethics

- Never suggests manipulation, gaslighting, or PUA tactics
- Blocks sensitive topics (breakup, money, sex, marriage) from autopilot
- Requires explicit confirmation before sending anything
- Gives graceful exit strategies for unhealthy dynamics

### License

MIT License — free for personal and commercial use.

---

## 中文

### 这是什么？

love-agent 是一个闭环 AI 恋爱军师技能。分析聊天消息、预测回复效果、生成情境化的回复建议。为认真对待感情的人提供策略性、基于证据的沟通指导——不是通用的撩妹话术。

### 核心流水线（10步）

```
观察 → 记忆 → 解读 → 判断 → 战略 → 生成 → 模拟 → 批评 → 修正 → 决策 → 发送 → 更新记忆
```

每步都有独立 LLM prompt，用**证据链推理**（置信度评分、来源标注）而非主观猜测。

### 主要功能

| 功能 | 说明 |
|------|------|
| 🧠 **关系阶段检测** | 识别关系阶段：陌生→认识→暧昧→追求→恋爱→冲突→分手→复合 |
| 💬 **情境化回复** | 根据你的人设和对方性格生成回复 |
| 🔮 **反应模拟** | 模拟对方可能的反应和解读 |
| 🛡️ **批评修正循环** | 12项安全检查，自动修正不当回复 |
| 📝 **长期记忆** | 人物卡片系统 + 自动标签存储 |
| 🏷️ **自动标签提取** | 自动识别并存储聊天中的关键信息 |
| 📱 **多模态输入** | 支持文字、图片(OCR)、语音(转写)、截图 |
| ⚙️ **三种模式** | suggest(只建议)/confirm(确认后发)/autopilot(自动发送) |

### 快速开始

```bash
# 安装
pip install -r requirements.txt

# 运行测试
python tests/run_tests.py

# 分析消息
python bin/love_agent.py --content "对方说的话" --mode suggest
```

### 人物卡片系统

每个暧昧对象独立一张卡片：
- `person_001` = 二妹
- `person_002` = 下一个
- 每张卡片隔离存储，不会串用

### 自动标签类别

分析时自动提取存储：工作、收入、所在地、爱好、教育、家庭、感情历史、性格细节、生活习惯、价值观、说话风格、忌讳话题、约会偏好、社交圈、未来计划等 19 类。

### 安全与伦理

- 不提供操控、煤气灯、PUA 技巧
- 敏感话题（分手/金钱/性/婚姻）禁止自动发送
- 发送前必须确认
- 不健康关系提供体面退出策略

---

## 日本語

### love-agent とは？

愛の対話 Strategist AI スキル。チャットメッセージを分析し、返信の効果を予測し、文脈に合わせた返信提案を生成します。戦略的で証拠に基づくコミュニケーションアドバイスを求めます。

### コアパイプライン

```
観察 → 記憶 → 解釈 → 推定 → 戦略 → 生成 → シミュレーション → 批判 → 修正 → 決定 → 送信 → 記憶更新
```

### 主な機能

| 機能 | 説明 |
|------|------|
| 🧠 **関係ステージ検出** | 陌生人→友人→暧昧→追求→恋愛→衝突→別れ→復合 |
| 💬 **文脈対応返信** | あなたの人設と相手の性格に合わせた返信を生成 |
| 🔮 **反応シミュレーション** | 相手がどう反応するかをシミュレート |
| 🛡️ **批判・修正ループ** | 12項目の安全チェック、自動修正 |
| 📝 **長期記憶** | 人物カードシステム + 自動タグ保存 |
| 🏷️ **自動タグ抽出** | 会話から重要な情報を自動提取・保存 |
| 📱 **マルチモーダル** | テキスト、画像(OCR)、音声(文字起こし)、スクリーンショット対応 |
| ⚙️ **3つのモード** | suggest(提案のみ)/confirm(確認後送信)/autopilot(自動送信) |

---

## 한국어

### love-agent란?

대화 전략 AI 스킬. 채팅 메시지를 분석하고, 응답 효과를 예측하며, 상황에 맞는 답변을 제안합니다. 증거 기반의 전략적 커뮤니케이션 조언을 원한다면.

### 핵심 파이프라인

```
관찰 → 기억 → 해석 → 추정 → 전략 → 생성 → 시뮬레이션 → 비판 → 수정 → 결정 → 전송 → 기억 업데이트
```

### 주요 기능

| 기능 | 설명 |
|------|------|
| 🧠 **관계 단계 감지** | 낯섦→知り合い→暧昧→추구→연애→갈등→이별→화해 |
| 💬 **상황 대응 답변** | 당신의 페르소나와 상대방 성격에 맞는 답변 생성 |
| 🔮 **반응 시뮬레이션** | 상대방의 가능한 반응 시뮬레이션 |
| 🛡️ **비판·수정 루프** | 12항목 안전 체크, 자동 수정 |
| 📝 **장기 기억** | 인물 카드 시스템 + 자동 태그 저장 |
| 🏷️ **자동 태그 추출** | 대화에서 핵심 정보 자동 추출·저장 |
| 📱 **멀티모달** | 텍스트, 이미지(OCR), 음성(음성인식), 스크린샷 지원 |
| ⚙️ **3가지 모드** | suggest(제안만)/confirm(확인 후 전송)/autopilot(자동 전송) |

---

## Español

### ¿Qué es love-agent?

Un asesor de relaciones con IA en bucle cerrado. Analiza mensajes de chat, predice resultados de respuestas y genera sugerencias contextualizadas. Para quienes buscan comunicación estratégica y basada en evidencia.

### Pipeline principal

```
Observar → Recordar → Interpretar → Estimar → Estrategizar → Generar → Simular → Criticar → Revisar → Decidir → Enviar → Actualizar memoria
```

### Características principales

| Característica | Descripción |
|----------------|-------------|
| 🧠 **Detección de etapa relacional** | Desconocido→Acuaintance→Flirting→Courting→Dating→Conflict→Breakup→Reconciliation |
| 💬 **Respuestas contextualizadas** | Genera respuestas según tu persona y la del otro |
| 🔮 **Simulación de reacciones** | Simula cómo podría reaccionar la otra persona |
| 🛡️ **Ciclo crítico-revisión** | 12 puntos de seguridad, revisión automática |
| 📝 **Memoria a largo plazo** | Sistema de tarjetas por persona + tags automáticos |
| 🏷️ **Extracción automática** | Extrae y almacena información clave automáticamente |
| 📱 **Multi-modal** | Soporta texto, imágenes (OCR), voz, capturas |
| ⚙️ **Tres modos** | suggest (solo sugerir)/confirm (confirmar antes)/autopilot (auto-enviar) |

---

## Français

### Qu'est-ce que love-agent ?

Un conseiller relationnel IA en boucle fermée. Analyse les messages, prédit les réponses, génère des suggestions contextuelles. Pour une communication stratégique et fondée sur des preuves.

### Pipeline principal

```
Observer → Se souvenir → Interpréter → Estimer → Stratégiser → Générer → Simuler → Critiquer → Réviser → Décider → Envoyer → Mettre à jour la mémoire
```

### Fonctionnalités

| Fonctionnalité | Description |
|----------------|-------------|
| 🧠 **Détection de stade relationnel** | Étranger→Connaissance→Flirt→Cour→Dating→Conflit→Breakup→Réconciliation |
| 💬 **Réponses contextuelles** | Génère selon ta persona et celle de l'autre |
| 🔮 **Simulation de réactions** | Simule comment l'autre pourrait réagir |
| 🛡️ **Boucle critique-révision** | 12 points de sécurité, révision auto |
| 📝 **Mémoire long terme** | Système de cartes par personne + tags auto |
| 🏷️ **Extraction auto** | Extrait et stocke les infos clés auto |
| 📱 **Multi-modal** | Texte, images (OCR), voix, screenshots |
| ⚙️ **Trois modes** | suggest (suggestions)/confirm (confirmer)/autopilot (auto) |

---

## Deutsch

### Was ist love-agent?

Ein KI-Beziehungsberater im geschlossenen Kreislauf. Analysiert Chat-Nachrichten, sagt Antwortwirkungen voraus und generiert kontextbewusste Vorschläge. Für strategische, evidenzbasierte Kommunikation.

### Kern-Pipeline

```
Beobachten → Erinnern → Interpretieren → Einschätzen → Strateisieren → Generieren → Simulieren → Kritik → Überarbeiten → Entscheiden → Senden → Gedächtnis aktualisieren
```

### Hauptfunktionen

| Funktion | Beschreibung |
|----------|-------------|
| 🧠 **Beziehungsphasen-Erkennung** | Fremder→Bekannte→Flirt→Werben→Dating→Konflikt→Breakup→Versöhnung |
| 💬 **Kontextuelle Antworten** | Generiert basierend auf deiner Persona und der anderen Person |
| 🔮 **Reaktions-Simulation** | Simuliert mögliche Reaktionen |
| 🛡️ **Kritik-Überarbeitung** | 12 Sicherheitspunkte, auto-Überarbeitung |
| 📝 **Langzeitgedächtnis** | Personen-Kartensystem + Auto-Tags |
| 🏷️ **Auto-Extraktion** | Extrahiert und speichert Schlüsselinfos |
| 📱 **Multi-modal** | Text, Bilder (OCR), Stimme, Screenshots |
| ⚙️ **Drei Modi** | suggest (Vorschlag)/confirm (Bestätigen)/autopilot (Auto) |

---

## Tiếng Việt

### love-agent là gì?

Trợ lý AI quan hệ vòng kín. Phân tích tin nhắn, dự đoán phản hồi, tạo gợi ý phù hợp ngữ cảnh. Cho giao tiếp chiến lược dựa trên bằng chứng.

### Quy trình chính

```
Quan sát → Ghi nhớ → Diễn giải → Ước lượng → Lập chiến lược → Tạo → Mô phỏng → Phê bình → Sửa → Quyết định → Gửi → Cập nhật bộ nhớ
```

### Tính năng chính

| Tính năng | Mô tả |
|-----------|-------|
| 🧠 **Phát hiện giai đoạn** | Người lạ→quen→暧昧→theo đuổi→yêu→xung đột→chia tay→hòa giải |
| 💬 **Trả lời theo ngữ cảnh** | Theo persona của bạn và đối phương |
| 🔮 **Mô phỏng phản ứng** | Dự đoán cách đối phương phản ứng |
| 🛡️ **Kiểm tra an toàn** | 12 điểm kiểm tra, tự sửa |
| 📝 **Bộ nhớ dài hạn** | Thẻ người + Tags tự động |
| 🏷️ **Trích xuất tự động** | Tự lưu thông tin quan trọng |
| 📱 **Đa phương tiện** | Văn bản, ảnh (OCR), giọng nói, ảnh chụp |
| ⚙️ **3 chế độ** | suggest (gợi ý)/confirm (xác nhận)/autopilot (tự động) |

---

## Indonesia

### Apa itu love-agent?

Asisten AI hubungan loop tertutup. Menganalisis pesan, memprediksi balasan, membuat saran kontekstual. Untuk komunikasi strategis berbasis bukti.

### Pipeline utama

```
Amati → Ingat → Interpretasi → Estimasi → Strategi → Generate → Simulasi → Kritik → Revisi → Putuskan → Kirim → Update memori
```

### Fitur utama

| Fitur | Deskripsi |
|-------|-----------|
| 🧠 **Deteksi tahap** | Asing→kenalan→flirt→nembak→jadian→konflik→putus→raih kembali |
| 💬 **Balasan kontekstual** | Sesuai persona kamu dan dia |
| 🔮 **Simulasi reaksi** | Prediksi cara dia bereaksi |
| 🛡️ **Pemeriksaan keamanan** | 12 titik, auto-revisi |
| 📝 **Memori jangka panjang** | Kartu orang + Tags otomatis |
| 🏷️ **Ekstraksi otomatis** | Simpan info penting otomatis |
| 📱 **Multi-modal** | Teks, gambar (OCR), suara, screenshot |
| ⚙️ **3 mode** | suggest (saran)/confirm (konfirmasi)/autopilot (otomatis) |

---

## Thai

### love-agent คืออะไร?

ที่ปรึกษาความสัมพันธ์ AI แบบวนปิด. วิเคราะห์ข้อความ, คาดการณ์การตอบกลับ, สร้างข้อเสนอที่เหมาะสมตามบริบท. สำหรับการสื่อสารเชิงกลยุทธ์บนพื้นฐานหลักฐาน

### กระบวนการหลัก

```
สังเกต → จำ → interpret → ประเมิน → ยุทธวิธี → สร้าง → จำลอง → ตรวจสอบ → แก้ไข → ตัดสิน → ส่ง → อัปเดตความจำ
```

### คุณสมบัติหลัก

| คุณสมบัติ | รายละเอียด |
|-----------|-----------|
| 🧠 **ตรวจจับระยะ** | ต่างคน→รู้จัก→ flirting → ตะขอ → อยู่ด้วยกัน → ขัดแย้ง → เลิก → กลับมา |
| 💬 **คำตอบตามบริบท** | ตาม persona ของคุณและอีกฝ่าย |
| 🔮 **จำลองปฏิกิริยา** | คาดการณ์วิธีที่อีกฝ่ายจะตอบสนอง |
| 🛡️ **ตรวจสอบความปลอดภัย** | 12 จุด, แก้ไขอัตโนมัติ |
| 📝 **ความจำระยะยาว** | บัตรบุคคล + Tags อัตโนมัติ |
| 🏷️ **แยกข้อมูลอัตโนมัติ** | บันทึกข้อมูลสำคัญอัตโนมัติ |
| 📱 **Multi-modal** | ข้อความ, ภาพ (OCR), เสียง, screenshot |
| ⚙️ **3 โหมด** | suggest (แนะนำ)/confirm (ยืนยัน)/autopilot (อัตโนมัติ) |

---

## Installation

```bash
# Clone
git clone https://github.com/wumumofashi/love-agent.git
cd love-agent

# Install dependencies
pip install -r requirements.txt

# Run tests (24 scenarios, no external dependencies)
python tests/run_tests.py
```

## Usage

```bash
# Basic analysis
python bin/love_agent.py --content "对方的原话" --mode suggest

# With full context
python bin/love_agent.py --json '{"content":"...","person":{"user_age":"26","other_age":"24",...},"mode":"confirm"}'

# Interactive setup (fill in all required fields)
python bin/love_agent.py --setup person_001

# Import chat history
python bin/love_agent.py --import-history chat_history.txt --person-id person_001
```

## API

Requires an OpenAI-compatible endpoint. Set via environment variable:

```bash
export LOVE_AGENT_API_KEY="sk-..."
```

Or configure in `config/model.json`:

```json
{
  "provider": "openai_compatible",
  "base_url": "https://api.your-provider.com/v1",
  "model": "your-model",
  "api_key_env": "LOVE_AGENT_API_KEY"
}
```

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for full system design.

Key components:
- **Engine**: 10-step closed-loop pipeline
- **Memory**: Per-person card system with insights
- **Knowledge**: Tiered (A/B/C/D) evidence-based knowledge base
- **Reply**: Planner → Generator → Simulator → Critic → Revise chain

## Testing

```bash
# Full test suite
python tests/run_tests.py        # 24 scenario tests
python tests/test_llm_pipeline.py # LLM chain tests
python scripts/verify.py         # Harness verification
```

All 24 tests pass with zero external dependencies.

## Contributing

PRs welcome! Please read [docs/RESEARCH_COMPARISON.md](docs/RESEARCH_COMPARISON.md) and [docs/REUSE_ASSESSMENT.md](docs/REUSE_ASSESSMENT.md) before submitting.

## License

MIT License.

