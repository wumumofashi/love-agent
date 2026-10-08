from __future__ import annotations

def _short(text: str) -> str:
    return text.strip()

def generate_candidates(ctx: dict) -> list[dict]:
    intent=ctx.get("reply_intent","continue"); msg=ctx.get("current_message","")
    person=(ctx.get("person") or {}).get("name","")
    stage=ctx.get("relationship_stage","认识")
    mm=ctx.get("multimodal",{})
    c=[]
    def add(label,text,tone=""):
        if text and all(x["text"]!=text for x in c): c.append({"label":label,"text":_short(text),"intent":intent,"tone":tone or ctx.get("tone","")})
    if intent=="comfort":
        add("自然型","听起来今天是真的累着了。你先缓缓，不用硬撑，我在呢。")
        add("轻松型","先下班模式关机一会儿。吃点热的，剩下的明天再说。")
    elif intent=="low_pressure_reconnect":
        add("低风险","没事，你先忙你的。刚看到个有意思的，回头丢给你。")
        add("稳妥","好，那你先休息。想聊的时候喊我。")
    elif intent=="wait_or_light_ping":
        c.append({"label":"建议不发","text":"","intent":intent,"tone":"克制"})
        add("低风险","刚刷到一个你可能会笑的，先存着，你忙完再看。")
    elif intent=="reconcile_careful":
        add("低风险","我听到了。先别急着定，之前分开的那个问题，咱们得先说清楚。")
        add("稳妥","我不是不想，就是不想稀里糊涂又回到老样子。你愿意慢慢聊聊吗？")
    elif intent=="money_boundary":
        add("低风险","你先跟我说下是啥情况，大概需要多少？我看完再回复你。")
    elif intent=="acknowledge_subtext":
        add("自然型","你这句听着不像没事。是不是我刚哪里让你不舒服了？你直说就行。")
        add("稳妥","行，我先不猜。你想说的时候我在，不想说就先放一放。")
    elif intent=="warm_reciprocate":
        add("自然型","你还记得这个啊，被你投喂得很开心。下次换我来。")
        add("轻松型","收到了，这份心意我先记账了，必须回请。")
    elif intent=="light_flirt":
        add("自然型","你这样说，我会有点当真了啊。")
        add("轻松型","行，那我先记下了。欠我的，下次见面补。")
        if stage in ("暧昧","追求","恋爱","稳定恋爱"): add("暧昧型","那你得负责，我已经开始想下次见你了。")
    elif intent=="invite":
        add("自然型","这周末你要是有空，一起去试试那家你之前提过的店？没空也没事，咱们再约。")
        add("轻松型","我发现个地方感觉你会喜欢。周六下午有空一起去看看？")
    elif intent=="de-escalate":
        add("低风险","我先不争这个。你刚才那句，我听着是有点委屈，是我没顾上你的感受。")
        add("稳妥","等咱俩都平静点再说行吗？我不想越聊越冲。")
    elif intent=="clarify":
        add("自然型","我刚那句可能说得容易误会。我本意不是那个意思，是想说这事咱们可以慢慢商量。")
        add("稳妥","怕你误会，我补一句：我不是在怪你，就是想把话说清楚。")
    elif intent=="reassure_without_control":
        add("自然型","这事我跟你说清楚，省得你瞎想。他就是同事，那天是大家一起吃的饭。")
        add("稳妥","你在意这个，我其实挺开心的。以后这种场合我提前跟你说一声。")
    elif intent=="own_and_repair":
        add("自然型","这事是我的问题，我光顾着自己着急，没考虑你听着难受。对不起。")
        add("稳妥","你生气有道理。我不找借口了，今晚我把这事处理好，再跟你交代。")
    elif intent=="respect_and_clarify":
        add("低风险","好，我尊重你。这个决定我听到了，不会再缠着你问。")
        add("稳妥","如果之后你愿意把话说完，我听。不愿意，也就到这儿。")
    elif intent=="graceful_exit":
        add("低风险","明白，那我就不打扰了。祝你一切顺利。")
    elif intent=="respond_to_share":
        desc=mm.get("description","").removeprefix("一张").removeprefix("一段")
        if desc: add("自然型",f"这个{desc}看着就很舒服，你今天是专门去的还是路过拍的？")
        else: add("自然型","这张氛围真好，是你今天拍的吗？")
        add("轻松型","可以啊，这状态看着比昨天精神多了。")
    elif intent=="respond_to_voice":
        transcript=mm.get("transcript","")
        if transcript: add("自然型",f"听到了。你说的那个事我懂了，咱们就按你说的来。")
        else: add("低风险","我这边刚没听清，你这条语音方便打个字不？不想打也没事，我回头再听。")
    elif intent=="respond_to_share" and mm.get("kind")=="video":
        add("自然型","视频里这个地方看着真不错，你去玩啦？")
    elif intent=="get_to_know":
        add("自然型","听起来你对这个还挺有研究的。入门的时候踩过什么坑没？")
        add("轻松型","这个我还真不太懂，你算是把我好奇心勾起来了。")
    elif intent=="maintain":
        add("自然型","行，那家里这个事就这么定。晚上回去咱们再把周末安排捋一下。")
    else:
        add("自然型","哈哈这个我能懂。我刚才还刷到个差不多的，回头给你看。")
        add("轻松型","你这一说我想起来了，上次那个事后来还真被你说中了。")
    # sensitive scenes: only low-risk pair
    flags=ctx.get("relationship_dynamics",{}).get("flags",[])
    if any(f in flags for f in ("conflict","breakup","rejection")):
        c=[x for x in c if x["label"] in ("低风险","稳妥")][:2]
    return c[:3]
