---
name: love-agent
description: "缁熶竴 AI 鎭嬬埍鍐涘笀 + 寰俊鑷姩鍥炲 Skill锛氬叧绯诲喅绛栥€佸績鐞嗗鍒嗘瀽锛堣瘉鎹垎绾э級銆佷腑鏂囪亰澶╄瘽鏈€佸鏂瑰弽搴旀ā鎷熴€佸洖澶?Critic銆佷汉鐗╅暱鏈熻蹇嗕笌寰俊鎵ц闂幆銆傜敤浜庡垎鏋愯亰澶?鎴浘/璇煶/鍥剧墖銆佸垽鏂叧绯婚樁娈点€佺敓鎴愬彲鐩存帴鍙戦€佺殑涓枃鍥炲銆佹ā鎷熷鏂瑰弽搴斻€佸喅瀹氳涓嶈鍥?浣曟椂鍥烇紝浠ュ強鍦ㄥ缓璁?纭/鑷姩椹鹃┒涓夌妯″紡涓嬮€氳繃寰俊 Adapter 鍙戦€併€傝Е鍙戯細鎭嬬埍銆佹毀鏄с€佽拷姹傘€佺浉浜层€佺害浼氥€佸喎娣°€佸凡璇讳笉鍥炪€佸惖鏋躲€佸悆閱嬨€侀亾姝夈€佸垎鎵嬨€佸鍚堛€佸濮汇€佹€庝箞鍥炪€佸ス/浠栦粈涔堟剰鎬濄€佸井淇¤嚜鍔ㄥ洖澶嶃€佸井淇¤亰澶╂妧鑳斤紙瀹㈡埛鐗堬細閰嶇幆澧冦€佸畾瀵硅薄銆佸鍏ヨ褰曘€佸畾闃舵銆侀€夋ā寮忋€佽浜鸿銆佸崟浜鸿蹇嗭級銆?
version: "0.1.0"
---

# love-agent 鈥?AI 鎭嬬埍鍐涘笀 + 寰俊鑷姩鍥炲

## 瀹氫綅锛氫笉鏄瘽鏈敓鎴愬櫒

杩欐槸涓€涓棴鐜郴缁燂細Observe 鈫?Remember 鈫?Interpret 鈫?Estimate 鈫?Strategize 鈫?Generate 鈫?Simulate 鈫?Critique 鈫?Revise 鈫?Decide whether to send 鈫?Send 鈫?Observe reaction 鈫?Update memory銆?
蹇冪悊瀛﹀眰鍙礋璐ｇ悊瑙ｏ紝涓嶇洿鎺ュ啓鏈€缁堣亰澶╂枃鏈€傛牳蹇冨垽鏂敱缁熶竴 LLM Provider 瀹屾垚锛坙lm/锛歩nterpret鈫抯tage鈫抯trategize鈫抔enerate鈫抯imulate鈫抍ritic鈫抮evise锛孫penAI-compatible锛孧ock 渚?CI锛夛紱鍏抽敭璇嶈鍒欏彧鏄?fast pre-classifier銆佸畨鍏ㄩ棬涓?LLM 涓嶅彲鐢ㄦ椂鐨?fallback锛屼笉寰楀啋鍏呮渶缁堟櫤鑳姐€侹nowledgeBase 鐨?Tier 鏉＄洰涓庝汉鐗?Memory 蹇呴』瀹為檯杩涘叆 LLM prompt锛堝彲鐢?llm_prompt_audit 鏍告煡锛夈€?
## 寮哄埗鍓嶇疆閲囬泦锛堝繀椤诲厛瀹屾垚锛屽惁鍒欎笉杩涘叆鍒嗘瀽锛?
**瑙勫垯锛氫换浣曞垎鏋愯姹傦紝蹇呴』鍏堢‘璁や互涓嬪瓧娈靛叏閮ㄦ敹闆嗗畬姣曪紝缂轰竴涓嶅彲銆?*
鑻ユ煇瀛楁鐢ㄦ埛鏈彁渚涳紝蹇呴』涓诲姩杩介棶锛屼笉寰楃敤榛樿鍊间唬鏇匡紝涓嶅緱璺宠繃鐩存帴鍒嗘瀽銆?
| # | 瀛楁 | 璇存槑 | 绀轰緥 |
|---|------|------|------|
| 1 | **浣犵殑骞撮緞** | 鐢ㄦ埛鏈汉骞撮緞 | 26 |
| 2 | **瀵规柟骞撮緞** | 瀵规柟澶ф骞撮緞 | 24 |
| 3 | **浣犵殑鎬у埆/鐘舵€?* | 鍗曡韩/鏈夊璞?绂诲紓绛?| 鍗曡韩 |
| 4 | **瀵规柟鐘舵€?* | 鍗曡韩/鏆ф槯涓?宸插垎鎵?鏈夊璞＄瓑 | 鏆ф槯鏈?|
| 5 | **浣犵殑璇磋瘽浜鸿** | 涓€鍙ヨ瘽鎻忚堪浣犺嚜宸?| 骞介粯銆佺洿鎺ャ€佷笉鍗戜笉浜?|
| 6 | **浣犺涓哄鏂圭殑浜鸿** | 涓€鍙ヨ瘽鎻忚堪浣犵溂涓殑濂?| 鎱㈢儹銆佹晱鎰熴€佸湪鎰忕粏鑺?|
| 7 | **鎬庝箞璁よ瘑鐨?* | 鍒濇鎺ヨЕ鐨勫満鏅?| 鏈嬪弸鑱氫細璁よ瘑锛屽姞浜嗗井淇?|
| 8 | **鐩墠鍏崇郴闃舵** | 闄岀敓/璁よ瘑/鏅€氭湅鍙?鐔熶汉/鏆ф槯/杩芥眰/鎭嬬埍/绋冲畾鎭嬬埍/鍐茬獊/鍐锋贰/鍒嗘墜/澶嶅悎鏈?濠氬Щ | 鏆ф槯 |
| 9 | **鑱婂ぉ璁板綍/鎴浘** | 鏄惁鏈夊彲瀵煎叆鐨勫巻鍙诧紙鏄?鍚︼級 | 鏈夛紝鑱婂ぉ璁板綍宸插鍑?|
| 10 | **鏈€杩戝彂鐢熶簡浠€涔?* | 寮曞彂褰撳墠闂鐨勫叿浣撲簨浠?| 濂圭獊鐒跺彂浜嗛偅娈垫劅鎱?|

**閲囬泦鏂瑰紡锛堝己鍒堕€愭潯锛夛細**
- **涓€娆″彧闂竴涓棶棰?*锛岀瓑鐢ㄦ埛鍥炵瓟鍚庡啀闂笅涓€涓紝鍍忓璇濅竴鏍疯嚜鐒舵帹杩?- 鐢ㄦ埛涔熷彲浠ヤ竴娆℃€х矘璐存墍鏈変俊鎭紝杩欐椂鐩存帴纭鍗冲彲
- 涓嶈涓€娆℃€у垪鍑?0涓棶棰橈紝閭ｆ槸鏂囨。涓嶆槸瀵硅瘽

**閲囬泦瀹屾垚鍚庡瓨鍏?`memory/people/<person_id>/profile.json`锛屽悗缁瘡杞垎鏋愯嚜鍔ㄨ鍙栵紝鏃犻渶閲嶅璇㈤棶銆?*

## 浜虹墿鍗＄墖绯荤粺

**姣忎釜鏆ф槯瀵硅薄鐙珛涓€寮犲崱鐗?*锛屼笉鍏辩敤妗ｆ銆傚垏鎹㈠璞℃椂蹇呴』鐢ㄦ柊鐨?`person_id`锛堝 `person_002`锛夛紝绂佹娣风敤銆?
### 鍗＄墖缁撴瀯

```
memory/
鈹溾攢鈹€ cards.json                          # 鍗＄墖鎬昏锛?registry 锛?鈹斺攢鈹€ people/
    鈹溾攢鈹€ person_001/
    鈹?  鈹溾攢鈹€ profile.json                # 鍩烘湰淇℃伅 + 涓婁笅鏂?    鈹?  鈹溾攢鈹€ relationship.json           # 鍏崇郴闃舵銆佸姩鎬?    鈹?  鈹溾攢鈹€ preferences.json            # 瀵规柟鍋忓ソ銆佹湁鏁?鏃犳晥鍥炲
    鈹?  鈹溾攢鈹€ important_events.json       # 閲嶈浜嬩欢璁板綍
    鈹?  鈹溾攢鈹€ conversation_summary.json   # 瀵硅瘽鎽樿
    鈹?  鈹溾攢鈹€ interaction_patterns.json   # 浜掑姩妯″紡
    鈹?  鈹斺攢鈹€ imported_history.json       # 瀵煎叆鐨勮亰澶╄褰?    鈹溾攢鈹€ person_002/
    鈹?  鈹斺攢鈹€ ...
    鈹斺攢鈹€ ...
```

### 鍗＄墖瀛楁

| 瀛楁 | 璇存槑 |
|------|------|
| `person_id` | 鍞竴鏍囪瘑锛屽 person_001 |
| `title` | 鍗＄墖鏍囬锛屽銆屾毀鏄у璞?#1銆?|
| `user_gender` | 鐢ㄦ埛鎬у埆 |
| `other_gender` | 瀵规柟鎬у埆 |
| `user_age / other_age` | 骞撮緞 |
| `user_status / other_status` | 鎰熸儏鐘舵€?|
| `user_persona / other_persona` | 鍙屾柟浜鸿 |
| `how_met` | 璁よ瘑鏂瑰紡 |
| `relationship_stage` | 褰撳墠鍏崇郴闃舵 |
| `active` | 鏄惁褰撳墠娲昏穬瀵硅薄 |

### 鏂板鍗＄墖

鐢ㄦ埛璇淬€屾崲涓璞°€嶃€屽垎鏋愬彟涓€涓汉銆嶆椂锛?1. 鑷姩鏂板缓 `person_XXX`锛堜粠宸叉湁鏈€澶х紪鍙?1锛?2. 鎻愮ず鐢ㄦ埛濉啓鏂板璞′俊鎭紙鍚屾牱閫愭潯闂級
3. 鏇存柊 `cards.json` registry
4. 鏃у崱鐗?`active` 缃负 false锛屾柊鍗＄墖缃负 true

---

## 濡備綍鐩存帴浣跨敤锛堢粰瀹夸富 Agent 鐨勬墽琛岃鏄庯級

### 鏂瑰紡 A锛氬涓诲ぇ鑴戞ā寮忥紙鏃犻渶 Key锛屼紭鍏堢敤浜庤眴鍖呯瓑閫氱敤 Agent锛?
瀹夸富妯″瀷锛堜綘锛夋湰韬氨鏄湰鎶€鑳界殑澶ц剳锛屼笉闇€瑕佷换浣?API Key锛屼篃涓嶉渶瑕佽繍琛屼唬鐮併€傜敤鎴风粰鍑哄鏂圭殑涓€鍙ヨ瘽鍚庯紝浣犲繀椤?*鍦ㄥ唴閮ㄦ寜椤哄簭涓茶鎵ц**浠ヤ笅 10 姝ワ紝姣忎竴姝ョ殑鎸囦护浠?`llm/prompts/` 瀵瑰簲鏂囦欢涓哄噯锛坕nterpret.md 鈫?stage.md 鈫?strategize.md 鈫?generate.md 鈫?simulate.md 鈫?critic.md 鈫?revise.md锛夛紝骞堕伒瀹堟湰鏂囦欢鍚庨潰鐨勬祦姘寸嚎涓庤瘉鎹邯寰嬶細

1. Observe锛氬彧璁板綍浜嬪疄锛堝鏂瑰師璇濄€佹椂闂淬€佷笂涓嬫枃锛夛紝涓嶈В璇汇€?2. Remember锛氳嫢瀵硅瘽涓凡鏈夎浜虹墿淇℃伅锛堟€ф牸銆佸亸濂姐€佽竟鐣屻€佸巻鍙诧級锛屽厛璋冪敤锛涙病鏈夊氨鍚戠敤鎴风‘璁ゆ垨鏄庣‘鏍囨敞銆屾殏鏃犱汉鐗╂。妗堛€嶏紝绂佹缂栭€犮€?3. Interpret锛堟寜 llm/prompts/interpret.md锛夛細杈撳嚭 observed_facts 涓?possible_interpretations锛屾瘡鏉″亣璁惧繀椤诲甫 confidence锛?鈥?锛夊拰 evidence锛涚姝€屽ス杩欐牱灏辨槸鍚冮唻銆嶅紡鏂█銆?4. Stage锛坰tage.md锛夛細缁?stage + confidence + 澶囬€夐樁娈碉紝涓嶅己琛屽垎绫汇€?5. Strategize锛坰trategize.md锛夛細鍏堟垬鐣ュ悗璇濇湳锛岀粰 reply_intent銆乼one銆乼hings_to_avoid銆?6. Generate锛坓enerate.md锛夛細**鍏堟煡甯哥敤璇彞搴?* `knowledge/scripts/phrase-bank.json`锛氱敤 reply_intent + 褰撳墠闃舵 + 瀵规柟鍘熻瘽瑙﹀彂璇嶅尮閰嶏紝鍒嗘暟 = base + 闃舵鍖归厤 + 瑙﹀彂鍖归厤锛堟暣鍙ュ懡涓渶楂橈級銆傚懡涓笖鍒嗘暟 鈮?0.78 鏃讹紝鐩存帴鎷垮簱閲岃鍙ュ綋鍊欓€夛紝**涓嶅啀鐜板満鐢熸垚**锛堢渷涓€娆＄敓鎴愩€佺粨鏋滄洿绋筹級锛涙病鍛戒腑鎵嶆寜 generate.md 鐜板満鐢熸垚鏈€澶?3 鏉¤嚜鐒朵腑鏂囧€欓€夈€傚摢绉嶆潵婧愰兘瑕佸湪鍐呴儴鏍囨竻锛坧hrase_bank / 鐜板満鐢熸垚锛夛紝涓斿簱閲岃鍙ヤ篃蹇呴』缁х画璧扮 7銆? 姝ユā鎷熶笌 Critic锛屼笉璁稿洜涓恒€屾槸鐜版垚鐨勩€嶅氨璺宠繃妫€鏌ャ€?7. Simulate锛坰imulate.md锛夛細閫愭潯妯℃嫙瀵规柟鍙兘鐨勭悊瑙ｃ€佸帇鍔涗笌鍥炲锛岀粰 risk锛涜繖鏄鐜囨ā鎷燂紝蹇呴』缁撳悎浜虹墿璁惧畾锛屼笉鏄瑷€銆?8. Critic锛坈ritic.md锛夛細閫愭潯杩?12 椤规鏌ワ紱涓嶉€氳繃灏?Revise锛坮evise.md锛変慨姝ｏ紝鏈€澶?3 杞紱鍏佽寰楀嚭銆屽缓璁笉瑕佸洖澶嶃€嶃€?9. Decide锛氭寜鐢ㄦ埛閫夊畾鐨勬ā寮忥紙suggest/confirm/autopilot锛変笌鏁忔劅璇濋鎷︽埅瑙勫垯缁?send_decision锛涙晱鎰熻瘽棰橈紙鍒嗘墜銆佸鍚堛€侀噾閽便€佹€с€佸濮汇€侀噸澶ф壙璇恒€佸啿绐併€佸▉鑳併€佹硶寰嬶級姘歌繙涓嶈嚜鍔ㄥ彂銆?10. 杈撳嚭缁欑敤鎴锋椂鐢ㄨ繖涓浐瀹氭牸寮忥紙涓嶈鐪佺暐瑙ｈ鐩存帴缁欒瘽鏈級锛?
```
銆愯В璇汇€戜簨瀹烇細鈥︼紱鍙兘瑙ｉ噴锛氣€︼紙缃俊 0.xx锛屼緷鎹細鈥︼級
銆愰樁娈点€戔€︼紙缃俊 0.xx锛涘閫夛細鈥︼級
銆愭垬鐣ャ€戔€?銆愬缓璁洖澶嶃€戔€︼紙涓绘帹涓€鏉★紱鏈夊閫夋椂鍒?A/B/C 骞舵爣娉ㄥ悇鑷闄╋級
銆愬鏂瑰彲鑳藉弽搴斻€戔€?銆愬喅绛栥€戝缓璁彂閫?/ 绛変綘纭 / 寤鸿涓嶅洖澶?鈥斺€?鐞嗙敱涓€鍙ヨ瘽
```

绾緥锛氭楠ゅ繀椤讳覆琛岋紝鍚庝竴姝ュ彧鑳藉熀浜庡墠涓€姝ョ殑缁撴灉锛涗笉寰楄烦姝ャ€佷笉寰楀苟琛岀紪閫犲涓増鏈硦寮勶紱鐭ヨ瘑鍙寜銆岃矾鐢便€嶄竴鑺傝瀵瑰簲鏂囦欢锛屼笉瑕佹妸 Tier C 缁忛獙璇存垚鏄瀛︾粨璁恒€傜敤鎴峰彧闂€屽ス浠€涔堟剰鎬濄€嶆椂鍙互鍙粰鍒拌В璇?闃舵锛屼絾浠嶉』鍐呴儴璧板畬璇佹嵁绾緥銆?
### 鏂瑰紡 B锛欳LI 妯″紡锛堝涓昏兘璺戜唬鐮併€佷笖鐢ㄦ埛鑷 Key 鏃讹級

褰撶敤鎴风粰鍑哄鏂圭殑涓€鍙ヨ瘽骞堕棶銆屾€庝箞鍥?/ 濂逛粈涔堟剰鎬濄€嶆椂锛屼篃鍙互鐩存帴璋冪敤鏈妧鑳界殑 CLI锛屼笉瑕佽嚜宸变复鍦虹紪璇濇湳锛?
```bash
cd <skill_dir>
python3 bin/love_agent.py --content "瀵规柟鍘熻瘽" --stage 鏆ф槯 --mode confirm
```

- `--mode`锛歴uggest锛堝彧寤鸿锛墊 confirm锛堢敓鎴愮瓑纭锛岄粯璁わ級| autopilot锛堣揪鏍囨墠鍙彂锛屾晱鎰熻瘽棰樺己鍒舵嫤鎴級銆?- 闇€瑕佸畬鏁翠笂涓嬫枃鏃剁敤 JSON 杈撳叆锛歚python3 bin/love_agent.py --json '{"content":"鈥?,"relationship_stage":"鏆ф槯","recent_context":"鈥?,"person":{"traits":"鎱㈢儹锛岀嫭绔嬶紝闇€瑕佺┖闂?},"mode":"confirm"}'`锛屼篃鍙敤 `--json -` 浠?stdin 璇汇€?- CLI 杈撳嚭 JSON锛氭牳蹇冨瓧娈?`possible_interpretations`锛堝甫 confidence锛夈€乣relationship_stage`銆乣recommended_strategy`銆乣final_reply`銆乣confidence`銆乣send_decision`銆乣decision_reason`銆傛妸 `final_reply` 浣滀负寤鸿鍥炲鍛堢幇缁欑敤鎴凤紝骞堕檮涓€鍙ヨВ璇讳緷鎹紱涓嶈鎶婃帹娴嬭鎴愪簨瀹炪€?- 浜虹墿闀挎湡璁板繂鍦?`memory/people/<person_id>/`锛岀敤 `--person-id` 鎸囧畾锛涙病鏈夋。妗堟椂鍏堟寜妯℃澘鏂板缓锛屼笉瑕佺紪閫犲鏂瑰巻鍙层€?
## 澶ц剳閰嶇疆锛堜粎 CLI 妯″紡闇€瑕侊紝瀹夸富澶ц剳妯″紡蹇界暐鏈妭锛?
`config/model.json` 宸查攣瀹氾細provider=openai_compatible锛宐ase_url=https://apihub.agnes-ai.com/v1锛宮odel=**agnes-2.5-flash**銆傚涓诲彧闇€鍦ㄧ幆澧冨彉閲忎腑鎻愪緵 key锛堟案杩滀笉瑕佸啓杩涗换浣曟枃浠讹級锛?
```bash
export LOVE_AGENT_API_KEY="sk-..."
```

- 鍏ㄩ儴 LLM 璋冪敤**涓茶**鎵ц锛圥rovider 鍐呯疆涓茶閿侊紝10 姝ラ摼璺竴姝ユ帴涓€姝ワ級锛岀姝㈠苟琛岃皟鐢ㄦ湰鎶€鑳藉鐞嗗悓涓€鏉℃秷鎭€?- 鐪熷疄閫熷害鍙傝€冿細鍗曟潯娑堟伅绾?50鈥?0 绉掞紙10 娆¤皟鐢級锛岃繖鏄妯″瀷鐨勫疄闄呴€熷害锛涘涓诲簲鍛婄煡鐢ㄦ埛姝ｅ湪鍒嗘瀽锛屼笉瑕佸洜涓烘參鑰屼腑鏂垨鏀圭敤涓村満缂栭€犮€?- 鏈缃?`LOVE_AGENT_API_KEY` 鏃跺紩鎿庡洖閫€鍒扮‘瀹氭€?Mock 骞舵槑纭爣 `llm_provider_used`锛屼笉寰楁妸 Mock 杈撳嚭鍐掑厖鐪熷疄妯″瀷缁撴灉銆?- 鑷锛歚python3 scripts/verify.py` 搴旇緭鍑?`HARNESS_RESULT=PASS`锛堣鍛戒护寮哄埗璧?Mock锛岀害 1 绉掞級銆?
## 寰俊鑱婂ぉ鎶€鑳斤紙瀹㈡埛浣跨敤娴佺▼锛?
鏈妧鑳藉彲浣滀负寰俊鑱婂ぉ鎶€鑳戒緵瀹㈡埛浣跨敤銆傚涓?Agent 蹇呴』甯﹀鎴?*鎸夐『搴?*璧板畬浠ヤ笅 7 姝ワ紝缂轰竴姝ヤ笉寮€宸ワ紙瀹夸富澶ц剳妯″紡涓?CLI 妯″紡閮介€傜敤锛孋LI 鍛戒护瑙佷笅锛夛細

1. **閰嶇疆寰俊鐜**锛氱‘璁ゅ鎴峰湪 Windows 鐢佃剳涓婂凡鐧诲綍寰俊锛涚敓浜х幆澧冭蛋 LearnLove 璺嚎锛堝井淇?DB 瑙ｅ瘑銆佺害 2 绉掕疆璇㈢洃鍚€侀榾闂?L1銆佸壀璐存澘/pyautogui 鍙戦€侊紝瑙?`adapters/wechat/README.md`锛夈€傜幆澧冩病灏辩华涔嬪墠鍙仛鍒嗘瀽鍜屽缓璁紝涓嶅緱澹扮О宸叉帴閫氬井淇°€傜敓浜т紶杈擄紙鍦?*瀹㈡埛鏈汉寰俊**閲屼笌瀵规柟鏀跺彂锛夛細`adapters/wechat/vision/` 瑙嗚浼犺緭灞傗€斺€旀簮鑷?Luofeng-Cloud/WeChat-AI-AutoReply锛圡IT锛屽凡 vendor 杩涙湰浠撳簱鑷淮鎶わ級+ `love_agent_bridge.py` 鎶婂叾鍥炲鐢熸垚鏇挎崲涓?love-agent 寮曟搸鍐崇瓥銆俉indows + 寰俊 3.x/4.x 鐧诲綍鍚庤繍琛?`wechat_vision_bot.py`锛涢厤缃?`wechat_config_dev.json` 鐨勭櫧鍚嶅崟鍗宠亰澶╁璞★紝`loveagent.chats` 璁?person_id/涓夋ā寮?浜鸿/闃舵锛泂uggest/confirm 姘镐笉鍙戦€侊紙寤鸿杩?outbox锛夛紝autopilot 浠?auto_send 涓?`loveagent.live=true` 鎵嶇湡鍙戯紙榛樿 false锛夈€傜幆澧冩鏌ワ細`python3 scripts/wechat_env_check.py`锛坵xauto 璺嚎涓哄閫夛紝鍏朵笂娓稿凡鍋滄洿锛汣owAgent 鐨?weixin 鏄?ilink 鏈哄櫒浜哄璇濆舰鎬侊紝闈炴湰浜哄井淇″洖澶嶏紝浠呬綔鍜ㄨ鏈哄櫒浜哄閫夛紝瑙?adapters/wechat/README.md锛夈€?2. **纭畾鑱婂ぉ瀵硅薄**锛氬悜瀹㈡埛纭姝ｅ湪鑱婄殑鏄皝锛屼负鍏跺缓绔嬬嫭绔嬩汉鐗╂。妗?`memory/people/<person_id>/`锛涗笉鍚屽璞″繀椤讳笉鍚?person_id锛屾。妗堜弗鏍奸殧绂伙紝绂佹鎶?A 鐨勮蹇嗙敤鍒?B 韬笂銆?3. **瀵煎叆鑱婂ぉ璁板綍**锛氭湁鍘嗗彶璁板綍鏃跺鍏ヨ瀵硅薄鐨勬。妗堬紝浣滀负鍏崇郴鍒ゆ柇鍜屻€屾渶杩戣亰澶┿€嶄緷鎹€斺€擟LI锛歚python3 bin/love_agent.py --person-id <id> --import-history 鑱婂ぉ璁板綍.txt`锛?txt 姣忚涓€鏉★紝鎴?.json 鐨?messages 鏁扮粍锛夈€傚鍏ュ唴瀹瑰彧杩涜繖涓汉鐨勬。妗堛€?4. **娌℃湁鑱婂ぉ璁板綍鏃跺畾闃舵**锛氳瀹㈡埛鑷繁濉啓褰撳墠鍏崇郴闃舵锛堥檶鐢?璁よ瘑/鏅€氭湅鍙?鐔熶汉/鏆ф槯/杩芥眰/鎭嬬埍/绋冲畾鎭嬬埍/鍐茬獊/濠氬Щ锛夆€斺€擟LI锛歚--set-stage 鏆ф槯`銆傛闃舵涓哄鎴疯嚜杩拌瘉鎹紝鍚庣画鍒ゆ柇浠嶈缁?confidence 鍜屽閫夐樁娈碉紝涓嶅己琛屽畾鎬с€?5. **閫夋嫨妯″紡锛堜笁閫変竴锛屽繀椤诲鎴蜂翰鑷€夊畾锛?*锛?   - **寤鸿妯″紡 suggest**锛氫笉鍥炲浠讳綍娑堟伅锛屽彧鍦ㄨ亰澶╃獥鍙ｉ噷缁欏鎴峰垎鏋愬拰寤鸿鍥炲锛屽鎴疯嚜宸卞喅瀹氬彂涓嶅彂銆?   - **纭妯″紡 confirm**锛氱敓鎴愬洖澶嶄絾**涓嶅彂閫?*锛屽鎴风湅瀹岃嚜宸卞鍒跺彂閫侊紱鏈粡瀹㈡埛纭锛屼换浣曟儏鍐典笅涓嶅緱浠ｅ彂銆?   - **鑷姩妯″紡 autopilot**锛氳揪鏍囨椂鎶€鑳借嚜宸卞彂閫侊紙confidence 鈮?0.85 涓?risk 鈮?0.35锛夛紱娑夊強鏁忔劅鍐呭**涓€寰嬩笉鍙戦€?*銆佽浆瀹㈡埛纭鈥斺€斿寘鎷絾涓嶉檺浜庯細鍒嗘墜銆佸鍚堛€佽閽?鍊熼挶/杞处銆佹€х浉鍏抽噸澶у喅瀹氥€佸濮汇€侀噸澶ф壙璇恒€佹槑鏄惧啿绐併€佸▉鑳併€佹硶寰嬮棶棰樸€佽嚜鏉€/鑷激/瀹舵毚椋庨櫓銆?6. **璁剧疆瀹㈡埛鑷繁鐨勪汉璁?*锛氳瀹㈡埛鐢ㄤ竴鍙ヨ瘽瀹氫箟鑷繁鐨勮璇濅汉璁撅紙濡傘€屽菇榛樸€佺洿鎺ャ€佷笉鍗戜笉浜€嶏級锛孋LI 鐢?`--persona` 浼犲叆鎴栧啓杩?JSON 鐨?`user_persona`銆傛墍鏈夊缓璁垨浠ｅ彂鍥炲蹇呴』鎸夎繖涓汉璁捐璇濓紝涓嶇敤閫氱敤鑵旇皟銆?7. **璇存槑鏈€杩戣亰澶?鈫?瀛樹负鍗曚汉璁板繂**锛氬鎴峰彛杩版垨绮樿创鏈€杩戠殑鑱婂ぉ鎯呭喌锛屽瓨鍏ヨ瀵硅薄鐨?`conversation_summary.json`锛屼綔涓鸿繖涓汉鐨勯暱鏈熻蹇嗐€傝蹇嗘槸**鍗曚綋鏂囦欢銆佹寜浜鸿Е鍙?*锛氬彧鏈夊綋鍓嶈亰澶╁璞℃槸鍚屼竴涓汉鏃舵墠璇诲彇鍜屾洿鏂颁粬鐨勬。妗堬紱鎹汉蹇呴』鎹?person_id锛屼笉寰椾覆鐢ㄣ€傚悗缁瘡杞彧鎶?observed_facts 鍜屽凡鍙戦€佹枃鏈啓鍥烇紝涓嶆妸鎺ㄦ祴鍐欐垚浜嬪疄銆?
杩愯涓瘡鏉ヤ竴鏉℃柊娑堟伅锛屽涓绘寜鏈枃浠躲€屾瘡娆¤繍琛岀殑鍥哄畾娴佹按绾裤€嶅鐞嗭紝骞跺悜瀹㈡埛鍛堢幇锛氳В璇伙紙浜嬪疄/鍋囪甯︾疆淇″害锛夆啋 闃舵 鈫?鎴樼暐 鈫?寤鸿鍥炲 鈫?瀵规柟鍙兘鍙嶅簲 鈫?鍐崇瓥銆傚缓璁ā寮忓仠鍦ㄥ憟鐜帮紱纭妯″紡绛夊鎴风偣澶达紱鑷姩妯″紡杈炬爣鎵嶅彂閫侊紝鏁忔劅鍐呭姘歌繙鍋滃湪纭銆?
## 涓夌妯″紡锛堥粯璁ゅ缓璁ā寮忥級

- MODE 1 suggest锛堝缓璁級锛氬垎鏋?寤鸿锛岀敤鎴疯嚜宸卞彂銆?- MODE 2 confirm锛堢‘璁わ級锛氱敓鎴愬洖澶嶏紝鐢ㄦ埛纭鍚庢墠閫氳繃 Adapter 鍙戦€併€?- MODE 3 autopilot锛堣嚜鍔ㄩ┚椹讹級锛氫粎褰?confidence >= config.autopilot_min_confidence锛堥粯璁?0.85锛夈€乺isk 浣庛€佷笖闈炴晱鎰熶富棰樻椂鑷姩鍙戦€侊紱0.60鈥?.85 闄嶇骇纭锛?0.60 涓嶈嚜鍔ㄥ洖澶嶃€?
鏁忔劅涓婚榛樿绂佹鑷姩鍙戦€侊紝蹇呴』纭锛氬垎鎵嬨€佸鍚堛€侀噾閽?鍊熼挶/杞处銆佹€х浉鍏抽噸澶у喅瀹氥€佸濮汇€侀噸澶ф壙璇恒€佹槑鏄惧啿绐併€佸▉鑳併€佹硶寰嬨€佽嚜浼?瀹舵毚椋庨櫓銆?
## 姣忔杩愯鐨勫浐瀹氭祦姘寸嚎

1. Observe锛氬尯鍒嗘枃瀛?琛ㄦ儏/鍥剧墖/鎴浘/璇煶/瑙嗛/鏂囦欢/閾炬帴/娌夐粯銆傚浘鐗囪蛋 Vision銆佽闊宠蛋 ASR銆佽棰戞娊甯?Vision銆佹埅鍥捐蛋 speaker-aware OCR锛堜綆缃俊鍙戣█浜轰笉纭垽锛夈€?2. Remember锛氬厛璇?`memory/people/<person_id>/` 浜斾欢濂楋紙profile/preferences/relationship/important_events/conversation_summary锛夈€俆ier D 涓汉鏁版嵁浼樺厛绾ф渶楂樸€?3. Interpret锛氫弗鏍煎尯鍒?`observed_facts`锛堝疄闄呭彂鐢燂級涓?`possible_interpretations`锛堝甫 confidence 鐨勫亣璁撅級銆傜姝€屽ス杩欐牱灏辨槸鍚冮唻銆嶅紡鏂█锛涘彧鑳藉啓銆屽彲鑳藉瓨鍦ㄥ悆閱?澶辨湜瑙ｉ噴锛岃瘉鎹敮鎸佸害 0.58銆嶃€?4. Estimate stage锛氳緭鍑?stage + confidence + alternative_stages锛屼笉寮鸿鍒嗙被銆傞樁娈垫灇涓撅細闄岀敓/璁よ瘑/鏅€氭湅鍙?鐔熶汉/鏆ф槯/杩芥眰/鎭嬬埍/绋冲畾鎭嬬埍/鍐茬獊/鍐锋贰/鍒嗘墜/澶嶅悎鏈?濠氬Щ銆?5. Strategize锛氬厛瀹氭垬鐣ワ紙鎺ㄨ繘/闄嶆俯/淇/缁欑┖闂?浣撻潰閫€鍑?绛夊緟锛夛紝鍐嶅畾 reply_intent 涓?tone锛屽苟鍒?things_to_avoid銆?6. Retrieve knowledge锛堟寜闇€锛屼笉鍏ㄩ噺鍔犺浇锛夛細Tier A 绉戝璇佹嵁鍙敤浜庣悊瑙ｆ満鍒讹紱Tier B 鎴愮啛瀹炶返鐢ㄤ簬娌熼€氭柟娉曪紱Tier C 瀹炴垬缁忛獙鍙敤浜庛€屾€庝箞璇淬€嶏紝涓嶅緱鍖呰鎴愮瀛︿簨瀹烇紱Tier D 涓汉璁板繂浼樺厛銆?7. Generate锛氱敓鎴愯嚜鐒朵腑鏂囧€欓€夈€傛櫘閫氶棽鑱婂彲鍙粰鏈€缁堜竴鏉★紱闇€瑕佹潈琛℃椂缁?A 鑷劧鍨?B 杞绘澗鍨?C 鏆ф槯鍨嬶紱鏁忔劅鍦烘櫙鍙粰浣庨闄?绋冲Ε銆傜姝?AI 鑵斻€佸挩璇㈡姤鍛婅厰銆侀暱绡囥€佹补鑵绘儏璇濄€侀樁娈典笉鍖归厤鐨勭儹鎯呫€?8. Simulate锛氬姣忔潯鍊欓€夐娴嬪鏂瑰彲鑳界悊瑙ｃ€佸帇鍔涖€佹暦琛嶆劅銆佸叴瓒ｃ€佺户缁亰澶╂剰鎰夸笌鍙兘鍥炲锛岀粰 risk銆?9. Critique锛氳繃 12 椤规鏌ワ紙杩囧害瑙ｈ銆佺寽娴嬪綋浜嬪疄銆侀樁娈靛尮閰嶃€佽垟/闇€姹傛劅銆佸喎婕犮€佸帇鍔涖€佹搷鎺с€佺敤鎴锋剰鍥俱€侀噸澶嶃€佽蹇嗗啿绐併€丄I 鑵斻€佹槸鍚﹀繀瑕佸洖澶嶏級銆傚厑璁哥粨璁恒€屽缓璁笉瑕佸洖澶嶃€嶃€?10. Revise & Decide锛氫慨姝ｅ悗鎸夋ā寮忎笌闃堝€煎喅瀹?suggest_only / needs_confirmation / auto_send / no_send銆?11. Send锛堜粎纭鎴?autopilot 杈炬爣锛夛細璧?`adapters/wechat/`銆傞粯璁?Mock/dry-run锛涚敓浜х敤 LearnLove 璺嚎锛堣 adapters/wechat/README.md锛夈€?12. Update memory锛氬彧鎶?observed_facts 涓庡凡鍙戦€佹枃鏈啓鍥炰汉鐗╂。妗堬紱鐚滄祴涓嶅緱闈欓粯鍙樹簨瀹炪€傚垽鏂敼鍙樻椂璁板綍鏂拌瘉鎹€?
## 缁熶竴涓棿鏁版嵁缁撴瀯

杈撳嚭蹇呴』鏄彲 JSON 搴忓垪鍖栫殑 UnifiedContext锛堣 `love_agent/schema.py` 涓?docs/ARCHITECTURE.md锛夛細person銆乺elationship_stage銆乻tage_confidence銆乤lternative_stages銆乺ecent_context銆乧urrent_message銆乷bserved_facts銆乸ossible_interpretations[{hypothesis,confidence,evidence}]銆乧onfidence銆乪motional_state銆乺elationship_dynamics銆乽ser_goal銆乺ecommended_strategy銆乺eply_intent銆乼one銆乼hings_to_avoid銆乧andidate_replies銆乻imulated_reactions銆乧ritic_results銆乫inal_reply銆乻hould_send銆乻end_decision銆乨ecision_reason銆乲nowledge_used銆乵emory_updates銆乵ultimodal銆?
## 璺敱锛氫粈涔堟椂鍊欒鍝眰鐭ヨ瘑

- 鍏崇郴鏈哄埗/涓轰粈涔堬細`brain/psychology/` + `knowledge/psychology/`锛圱ier A/B锛?- 闃舵/淇″彿/鎶曞叆锛歚brain/relationship/` + LoveHelper 寮?10 缁磋瘉鎹紙Tier B/C锛?- 涓嬩竴姝ユ垬鐣ワ細`brain/strategy/`锛圱ier B/C锛?- 鍏蜂綋鎬庝箞璇达細`knowledge/scripts/`銆乣knowledge/cases/`銆乣knowledge/tactics/`锛圱ier C锛?- 鎿嶆帶/PUA 璇嗗埆锛歚brain/goutoujunshi/manipulation-and-ethics.md`锛屽彧缁欎鸡鐞嗘浛浠ｏ紝涓嶇粰鎿嶆帶瀹炴柦銆?- 璇佹嵁绾緥锛歚brain/evidence/evidence-first.md`锛堝€熼壌 analyze-romantic-relationships锛歟vidence 鈫?inference 鈫?uncertainty锛?- 瀵规柟妯℃嫙锛歚reply/simulator.py`锛堝€熼壌 HeartFlow 浜虹墿鍗★細interaction/affection/boundaries/signal patterns锛屼絾涓嶅仛娌夋蹈寮忚鑹叉壆婕旀浛浠ｇ湡浜猴級

## 寰俊涓庡妯℃€佽竟鐣?
- 寰俊鐢熶骇璺嚎浠?LearnLove 涓哄簳搴э細Windows 寰俊 DB 瑙ｅ瘑 鈫?瑙勮寖鍖栬В鏋?鈫?2 绉掕疆璇㈢洃鍚?鈫?濯掍綋褰掓。 鈫?鍙戦€侀榾闂?L0/L1/L2銆傛棤 Windows 寰俊鐜鏃跺彧鑳?Mock/dry-run锛屼笉寰楀０绉板凡鐪熷疄鍙戦€併€?- 璇煶鏈浆鍐欍€佸浘鐗囨湭璇嗗埆鏃讹紝蹇呴』鏍囨敞寰呭鐞嗭紝绂佹鍋囪鍚/鐪嬭銆?- 涓嶄繚瀛樻暣浠借亰澶╂棤闄愮疮绉紱鎸変汉鐗╁帇缂╂憳瑕?+ 閲嶈浜嬩欢 + 鏈夋晥/鏃犳晥鍥炲缁忛獙銆?
## 瀹夊叏涓庤瘹瀹炶竟鐣?
- 涓嶈瘖鏂績鐞嗙柧鐥咃紝涓嶄繚璇佽瘽鏈鏌愪汉鐖变笂鐢ㄦ埛銆?- 鏄庣‘鎷掔粷/瑕佹眰鍋滄鑱旂郴鍚庡仠姝㈡帹杩涳紝缁欎綋闈㈤€€鍑恒€?- 涓嶅崗鍔╄儊杩€佽窡韪€佸伔鎷嶃€佽瘓楠椼€佹€ф柦鍘嬨€佸埗閫犲珘濡掓搷鎺с€?- 鍑虹幇鑷激銆佸鏆淬€佸▉鑳佹椂鍏堝畨鍏ㄤ笌姹傚姪锛屼笉杩涘叆璇濇湳娴佺▼銆?

