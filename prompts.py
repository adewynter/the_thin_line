"""
This one holds all the prompts + exemplars for this paper.
"""

base_prompt_c16 = "You will be given a transcript of two participants (P1, P2) having a debate.\nExtract and label the arguments for the last turn's statement (denoted by CURRENT) and label them.\nThis means that CURRENT may be comprised of an “argument” (a thesis, the point someone is making) and multiple sentences or premises (“reasons”).\nFirst extract every argument from CURRENT.\n- Arguments must be a complete sentence (start with a capital letter and end in “.”, “?”, “!”, etc) verbatim from the text.\n- Not all parts of CURRENT need to be arguments or reasons (for example “hi, I wish to discuss the elections” is neither).\n- Arguments can also lack supporting reasons (\"I don't believe climate change is bad\")\n- They also may be enthymemes, and implicitly refer to other parts of the dialogue (\"I disagree\"); or simply state a position (\"I wish to talk about tech's D&I policies and how they haven't moved the needle for inclusion\").\n- If there are no arguments, write N/A.\nAfter extracting the arguments, label them according to the criteria below."
base_prompt_c7 = "You will be given a transcript of two participants (P1, P2) having a debate.\nDetermine who won the debate based on persuasiveness of their arguments, ability to refute the opponent's arguments, and quality of their responses.\nNote that spelling and grammar are not relevant to this: only their debating abilities should matter here."

exemplar1 = "CURRENT: Hello. Here is what I was thinking the other day: socialism is good because it allows workers to democratically determine how to operate the workplace, and central planning allows for resources to be allocated in a useful way that market incentives may not be appropriate for. Capitalism is bad because it enables corporate greed and widening wealth inequality."
response1 = "Argument:\n\
socialism is good because it allows workers to democratically determine how to operate the workplace, and central planning allows for resources to be allocated in a useful way that market incentives may not be appropriate for.\n\
C-0: 2\nReason: there are reasons supporing the thesis\n\
C-1: 2\nReason: the reasons support the thesis\n\
C-2: 2\nReason: all reasons are relevant to the thesis\n\
C-3: 2\nReason: the reasons strengthen the conclusion\n\
C-4: 1\nReason: it could convince some listeners\n\
C-5: 2\nReason: there are no previous counterarguments\n\
C-6: 1\nReason: it is a good argument"

response1 += "\nArgument:\n\
Capitalism is bad because it enables corporate greed and widening wealth inequality.\n\
C-0: 2\nReason: there are reasons, only one, but there are, that supports the thesis\n\
C-1: 2\nReason: the reasons do support the thesis\n\
C-2: 2\nReason: all reasons are relevant to the thesis\n\
C-3: 1\nReason: the reasons do provide strength to the conclusion, but they aren’t good enough or sufficient\n\
C-4: 1\nReason: it could convince some\n\
C-5: 2\nReason: there are no previous counterarguments\n\
C-6: 0\nReason: it is not a strong argument"

exemplar2 = "P1: I have talked with women around our country. You want to talk about this is what people wanted? Pregnant women who want to carry a pregnancy to term suffering from a miscarriage, being denied care in an emergency room because the health care providers are afraid they might go to jail and she's bleeding out in a car in the parking lot? She didn't want that. Her husband didn't want that. A 12 or 13-year-old survivor of incest being forced to carry a pregnancy to term? They don't want that. And I pledge to you when Congress passes a bill to put back in place the protections of Roe v. Wade as president of the United States, I will proudly sign it into law. But understand, if Donald Trump were to be re-elected, he will sign a national abortion ban. Understand in his Project 2025 there would be a national abortion ban. Understand in his Project 2025 there would be a national abortion -- a monitor that would be monitoring your pregnancies, your miscarriages. I think the American people believe that certain freedoms, in particular the freedom to make decisions about one's own body, should not be made by the government."
exemplar2 += "\n\nCURRENT: Well, there she goes again. It's a lie. I'm not signing a ban. And there's no reason to sign a ban. Because we've gotten what everybody wanted. Democrats, Republicans and everybody else and every legal scholar wanted it to be brought back into the states. And the states are voting. And it may take a little time, but for 52 years this issue has torn our country apart. And they've wanted it back in the states. And I did something that nobody thought was possible. The states are now voting. What she says is an absolute lie. And as far as the abortion ban, no, I'm not in favor of abortion ban. But it doesn't matter because this issue has now been taken over by the states."
response2 = "Argument:\n\
It's a lie. I'm not signing a ban. And there's no reason to sign a ban. Because we've gotten what everybody wanted. Democrats, Republicans and everybody else and every legal scholar wanted it to be brought back into the states. And the states are voting. And it may take a little time, but for 52 years this issue has torn our country apart. And they've wanted it back in the states. And I did something that nobody thought was possible. The states are now voting. What she says is an absolute lie. And as far as the abortion ban, no, I'm not in favor of abortion ban. But it doesn't matter because this issue has now been taken over by the states.\n\
C-0: 2\nReason: there are reasons supporting the thesis\n\
C-1: 2\nReason: the reasons support the thesis\n\
C-2: 1\nReason: some reasons are not relevant to the thesis\n\
C-3: 1\nReason: the reasons do provide strength to the conclusion, but they aren’t good enough or sufficient\n\
C-4: 1\nReason: it could convince a few people\n\
C-5: 1\nReason: it addresses some early counterarguments\n\
C-6: 1\nReason: it is a weak argument"


exemplar3 = "P1: You are able to work a job and therefore that probably reflects that you work hard and is a valuable meritocratic trait for other people to have. As a result, we think that when people have money they’re going to use it to signal those other people in society, or they’re going to use it to chase the things that make them happy in the first place.\nOn this notion on how if someone sets up a foodbank, they won’t be seen as successful. Firstly again, we think that success is relative, just because you set up a food bank and haven’t made a Fortune 500 company doesn’t mean that you’re not successful. But on top of that, again we don’t think success is just tied to money because we say that CEOs are great people because they’ve made a huge contribution to society and presumably worked really hard to do it.\nIf you set up a food bank, you have done similar things. You’ve worked really hard and you’ve made a major contribution to society, we think people will still value those things and see them as a form of success. I’m going to be adding more analysis on happiness in our last piece of substantive, but I think that’s enough rebuttal for now."
exemplar3 += "\n\nP2: Then on the idea of minorities but before that, I’ll take that point.\nYour argument is that people will only compare against their own communities, rather than against TV, social media, or other forms of media. Therefore, your arguments about minorities rising up are infeasible.\n"
exemplar3 += "\n\nCURRENT: Why is this not the case? If a minority doesn’t think, I have to make a Fortune 500 company. They can still succeed relative within their communities and as a community as a whole, can make gradual steps forward. Yeah, they’re not going to become millionaires overnight, but you can have, for example, a community that sends almost no kids to university, starts to send a couple of kids every year.\nThat brings up perfectly this idea of minorities. They tell us, firstly it’s not about suffering. This was never about people starving on the streets, inequality still exists. The fact is that certain people have to work a minimum wage job, they might not be starving, but it is definitely less fair that they are much more likely to end up in a job that has more backbreaking labor for them, that means that they have less time to spend with their kids than someone who’s born into just a different zip code and therefore was far less likely to live that life."

response3 = "Argument:\n\
If a minority doesn’t think, I have to make a Fortune 500 company.\n\
C-0:\n0 Reason: No reasons given\n\
C-1:\n0 Reason: No reasons given\n\
C-2:\n0 Reason: No reasons given\n\
C-3:\n1 Reason: No reasons given\n\
C-4:\n0 Reason: it won't convince anyone\n\
C-5:\n0 Reason: it does not address any counterarguments\n\
C-6:\n-2 Reason: this argument is so bad it could harm the speaker's position"

response3 += "\nArgument:\n\
They can still succeed relative within their communities and as a community as a whole, can make gradual steps forward. Yeah, they’re not going to become millionaires overnight, but you can have, for example, a community that sends almost no kids to university, starts to send a couple of kids every year.\n\
C-0:\n2 Reason: there are reasons supporting the thesis\n\
C-1:\n2 Reason: the reasons support the thesis\n\
C-2:\n1 Reason: some reasons are not relevant to the thesis\n\
C-3:\n1 Reason: the reasons strengthen the conclusion, but they aren’t good enough or sufficient\n\
C-4:\n1 Reason: it could convince some people\n\
C-5:\n0 Reason: it addresses one possible counterargument\n\
C-6:\n-1 Reason: the argument is confrontational and could be detrimental to the speaker"

response3 += "\nArgument:\n\
That brings up perfectly this idea of minorities. They tell us, firstly it’s not about suffering.\n\
This was never about people starving on the streets, inequality still exists.\n\
The fact is that certain people have to work a minimum wage job, they might not be starving, but it is definitely less fair that they are much more likely to end up in a job that has more backbreaking labor for them, that means that they have less time to spend with their kids than someone who’s born into just a different zip code and therefore was far less likely to live that life.\n\
C-0:\n2 Reason: there are reasons supporting the thesis\n\
C-1:\n1 Reason: the reasons support the thesis, but are not complete.\n\
C-2:\n1 Reason: reasons are not entirely relevant to the thesis\n\
C-3:\n2 Reason: the reasons do provide strength to the conclusion\n\
C-4:\n2 Reason: it could convince people\n\
C-5:\n2 Reason: it addresses counterarguments\n\
C-6:\n2 Reason: it is a strong, though mostly persuasive, argument"


def get_annotator_prompt_c012(transcript, version, exemplars=True, sys_override=False, override=None, developer=False):
    '''
    Get a transcript and a criterion version (C-0, 1, 2).
    - Optionally request `exemplars` (for o3-based evals)
    - `sys_override` and `developer` to replace "system" with "user" or "developer"
    - `override` is for APO to replace the entire system prompt.
    '''

    c0_crit = "C-0: Are there reasons provided to support the thesis?\n- 2 if there are reasons to support the thesis.\n- 1 if there are some reasons, but it is hard to link them.\n- 0 if it is a thesis without supporting reasons."
    c1_crit = "C-1: Are the reasons consistent (not contradictory/mutually exclusive) with themselves or the thesis?\n- 2 if all reasons are consistent\n- 1 if some reasons are consistent\n- 0 if all reasons are inconsistent"
    c2_crit = "C-2: Are the reasons relevant to the thesis?\n- 2 if all reasons are relevant to the thesis\n- 1 if there are some reasons that are irrelevant to the thesis\n- 0 if no reason is relevant to the thesis"
    
    if version == "0":
        system_prompt = f"{base_prompt_c16}\n{c0_crit}"
    if version == "1":
        system_prompt = f"{base_prompt_c16}\n{c1_crit}"
    if version == "2":
        system_prompt = f"{base_prompt_c16}\n{c2_crit}"

    response1 = "Argument:\n\
    socialism is good because it allows workers to democratically determine how to operate the workplace, and central planning allows for resources to be allocated in a useful way that market incentives may not be appropriate for.\n"
    if version == "0":
        response1 += "C-0: 2\nReason: there are reasons supporing the thesis\n"
    if version == "1":
        response1 += "C-1: 2\nReason: the reasons support the thesis\n"
    if version == "2":
        response1 += "C-2: 2\nReason: all reasons are relevant to the thesis\n"

    response1 += "\nArgument:\n\
    Capitalism is bad because it enables corporate greed and widening wealth inequality.\n"
    if version == "0":
        response1 += "C-0: 2\nReason: there are reasons, only one, but there are, that supports the thesis\n"
    if version == "1":
        response1 += "C-1: 2\nReason: the reasons do support the thesis\n"
    if version == "2":
        response1 += "C-2: 2\nReason: all reasons are relevant to the thesis\n"

    response2 = "Argument:\n\
    It's a lie. I'm not signing a ban. And there's no reason to sign a ban. Because we've gotten what everybody wanted. Democrats, Republicans and everybody else and every legal scholar wanted it to be brought back into the states. And the states are voting. And it may take a little time, but for 52 years this issue has torn our country apart. And they've wanted it back in the states. And I did something that nobody thought was possible. The states are now voting. What she says is an absolute lie. And as far as the abortion ban, no, I'm not in favor of abortion ban. But it doesn't matter because this issue has now been taken over by the states.\n"
    if version == "0":
        response2 += "C-0: 2\nReason: there are reasons supporting the thesis\n"
    if version == "1":
        response2 += "C-1: 2\nReason: the reasons support the thesis\n"
    if version == "2":
        response2 += "C-2: 1\nReason: some reasons are not relevant to the thesis\n"
    
    response3 = "Argument:\n\
    If a minority doesn’t think, I have to make a Fortune 500 company.\n"
    response3 += "C-0:\n0 Reason: No reasons given\n"

    response3 += "\nArgument:\n\
    They can still succeed relative within their communities and as a community as a whole, can make gradual steps forward. Yeah, they’re not going to become millionaires overnight, but you can have, for example, a community that sends almost no kids to university, starts to send a couple of kids every year.\n"
    if version == "0":
        response3 += "C-0:\n2 Reason: there are reasons supporting the thesis\n"
    if version == "1":
        response3 += "C-1:\n2 Reason: the reasons support the thesis\n"
    if version == "2":
        response3 += "C-2:\n1 Reason: some reasons are not relevant to the thesis\n"
    
    response3 += "\nArgument:\n\
    That brings up perfectly this idea of minorities. They tell us, firstly it’s not about suffering.\n\
    This was never about people starving on the streets, inequality still exists.\n\
    The fact is that certain people have to work a minimum wage job, they might not be starving, but it is definitely less fair that they are much more likely to end up in a job that has more backbreaking labor for them, that means that they have less time to spend with their kids than someone who’s born into just a different zip code and therefore was far less likely to live that life.\n"
    if version == "0":
        response3 +=  "C-0:\n2 Reason: there are reasons supporting the thesis\n"
    if version == "1":
        response3 +=  "C-1:\n1 Reason: the reasons support the thesis, but are not complete.\n"
    if version == "2":
        response3 +=  "C-2:\n1 Reason: reasons are not entirely relevant to the thesis\n"

    skey = "system"
    if developer: skey = "developer"
    if sys_override: skey = "user"
    messages = [{"role": skey, "content": system_prompt if override is None else override}]
    if exemplars:
        messages += [
               {"role": "user", "content": exemplar1}, {"role": "assistant", "content": response1},
               {"role": "user", "content": exemplar2}, {"role": "assistant", "content": response2},
               {"role": "user", "content": exemplar3}, {"role": "assistant", "content": response3},
                ]

    messages.append({"role": "user", "content": transcript})
    
    return messages


def get_annotator_prompt_c3456(transcript, version, exemplars=True, override=None, sys_override=False, developer=False):
    '''
    Get a transcript and a criterion version (C-3, 4, 5, 6).
    - Optionally request `exemplars` (for o3-based evals)
    - `sys_override` and `developer` to replace "system" with "user" or "developer"
    - `override` is for APO to replace the entire system prompt.
    '''

    c3_crit = "C-3: Are the reasons supporting (provide strength/make the conclusion more likely) the thesis?\n- 2 if the reasons fully support the thesis\n- 1 if some reasons support the thesis\n- 0 if none of the reasons support the thesis"
    c4_crit = "C-4: How convincing is the argument?\n- 2 if the argument makes the conclusion very likely.\n- 1 if the conclusion is somewhat likely.\n- 0 if it is not likely."
    c5_crit = "C-5: Have the counterarguments, if any, been addressed? \nIf counterarguments were previously given:\n- 2 if all counterarguments were addressed.\n- 1 if some counterarguments were addressed.\n- 0 if neither counterargument has been addressed.\nIf no counterarguments were previously given, “2”."
    c6_crit = "C-6: (Is the argument winning?) Points to the participant:\n- 2 if it is a very good argument\n- 1 if it is a good argument\n- 0 if the argument does not sway their position towards a winning or losing position\n- -1 if it is a bad argument\n- -2 if it is a particularly bad argument"

    if version == "3":
        system_prompt = f"{base_prompt_c16}\n{c3_crit}"
    if version == "4":
        system_prompt = f"{base_prompt_c16}\n{c4_crit}"
    if version == "5":
        system_prompt = f"{base_prompt_c16}\n{c5_crit}"
    if version == "6":
        system_prompt = f"{base_prompt_c16}\n{c6_crit}"

    response1 = "Argument:\n\
    socialism is good because it allows workers to democratically determine how to operate the workplace, and central planning allows for resources to be allocated in a useful way that market incentives may not be appropriate for.\n"

    if version == "3":
        response1 += "C-3: 2\nReason: the reasons strengthen the conclusion\n"
    if version == "4":
        response1 += "C-4: 1\nReason: it could convince some listeners\n"
    if version == "5":
        response1 += "C-5: 2\nReason: there are no previous counterarguments\n"
    if version == "6":
        response1 += "C-6: 1\nReason: it is a good argument"
    
    response1 += "\nArgument:\n\
    Capitalism is bad because it enables corporate greed and widening wealth inequality.\n"
    if version == "3":
        response1 += "C-3: 1\nReason: the reasons do provide strength to the conclusion, but they aren’t good enough or sufficient\n"
    if version == "4":
        response1 += "C-4: 1\nReason: it could convince some\n"
    if version == "5":
        response1 += "C-5: 2\nReason: there are no previous counterarguments\n"
    if version == "6":
        response1 += "C-6: 0\nReason: it is not a strong argument"

    response2 = "Argument:\n\
    It's a lie. I'm not signing a ban. And there's no reason to sign a ban. Because we've gotten what everybody wanted. Democrats, Republicans and everybody else and every legal scholar wanted it to be brought back into the states. And the states are voting. And it may take a little time, but for 52 years this issue has torn our country apart. And they've wanted it back in the states. And I did something that nobody thought was possible. The states are now voting. What she says is an absolute lie. And as far as the abortion ban, no, I'm not in favor of abortion ban. But it doesn't matter because this issue has now been taken over by the states.\n"

    if version == "3":
        response2 += "C-3: 1\nReason: the reasons do provide strength to the conclusion, but they aren’t good enough or sufficient\n"
    if version == "4":
        response2 += "C-4: 1\nReason: it could convince a few people\n"
    if version == "5":
        response2 += "C-5: 1\nReason: it addresses some early counterarguments\n"
    if version == "6":
        response2 += "C-6: 1\nReason: it is a weak argument"
    
    response3 = "Argument:\n\
    If a minority doesn’t think, I have to make a Fortune 500 company.\n"
    if version == "3":
        response3 += "C-3:\n1 Reason: No reasons given\n"
    if version == "4":
        response3 += "C-4:\n0 Reason: it won't convince anyone\n"
    if version == "5":
        response3 += "C-5:\n0 Reason: it does not address any counterarguments\n"
    if version == "6":
        response3 += "C-6:\n-2 Reason: this argument is so bad it could harm the speaker's position"
    
    response3 += "\nArgument:\n\
    They can still succeed relative within their communities and as a community as a whole, can make gradual steps forward. Yeah, they’re not going to become millionaires overnight, but you can have, for example, a community that sends almost no kids to university, starts to send a couple of kids every year.\n"

    if version == "3":
        response3 += "C-3:\n1 Reason: the reasons strengthen the conclusion, but they aren’t good enough or sufficient\n"
    if version == "4":
        response3 += "C-4:\n1 Reason: it could convince some people\n"
    if version == "5":
        response3 += "C-5:\n0 Reason: it addresses one possible counterargument\n"
    if version == "6":
        response3 += "C-6:\n-1 Reason: the argument is confrontational and could be detrimental to the speaker"

    response3 += "\nArgument:\n\
    That brings up perfectly this idea of minorities. They tell us, firstly it’s not about suffering.\n\
    This was never about people starving on the streets, inequality still exists.\n\
    The fact is that certain people have to work a minimum wage job, they might not be starving, but it is definitely less fair that they are much more likely to end up in a job that has more backbreaking labor for them, that means that they have less time to spend with their kids than someone who’s born into just a different zip code and therefore was far less likely to live that life.\n"
    if version == "3":
        response3 += " C-3:\n2 Reason: the reasons do provide strength to the conclusion\n"
    if version == "4":
        response3 += " C-4:\n2 Reason: it could convince people\n"
    if version == "5":
        response3 += " C-5:\n2 Reason: it addresses counterarguments\n"
    if version == "6":
        response3 += " C-6:\n2 Reason: it is a strong, though mostly persuasive, argument"

    skey = "system"
    if developer: skey = "developer"
    if sys_override: skey = "user"
    messages = [{"role": skey, "content": system_prompt if override is None else override}]
    if exemplars:
        messages += [
               {"role": "user", "content": exemplar1}, {"role": "assistant", "content": response1},
               {"role": "user", "content": exemplar2}, {"role": "assistant", "content": response2},
               {"role": "user", "content": exemplar3}, {"role": "assistant", "content": response3},
                ]

    messages.append({"role": "user", "content": transcript})
    
    return messages


def get_annotator_prompt_c7(transcript, version, exemplars, override=None, sys_override=False, developer=False):
    '''
    Get a transcript and a version (for compatibility, unused) to determine the winner.
    - Optionally request `exemplars` (for o3-based evals)
    - `sys_override` and `developer` to replace "system" with "user" or "developer"
    - `override` is for APO to replace the entire system prompt.
    '''
    c7_crit = "C-7: Which player do you believe won the debate?\n- P1\n- P2\n- Draw. Give a reason for it in the form:"
    c7_crit += "Winner: \nReason:"

    c7_exemplar2 = exemplar2.replace("CURRENT", "P2")
    response2 = "Winner: P1\nReason: P1 made better, more convincing arguments"
    c7_exemplar3 = exemplar3.replace("CURRENT", "P1")
    response3 = "Winner: Draw\nReason: Both made very good points and my stance could not be completely swayed by either"

    system_prompt = f"{base_prompt_c7}\n{c7_crit}"

    skey = "system"
    if developer: skey = "developer"
    if sys_override: skey = "user"
    messages = [{"role": skey, "content": system_prompt if override is None else override}]
    if exemplars:
        messages += [
               {"role": "user", "content": exemplar1}, {"role": "assistant", "content": response1},
               {"role": "user", "content": c7_exemplar2}, {"role": "assistant", "content": response2},
               {"role": "user", "content": c7_exemplar3}, {"role": "assistant", "content": response3},
                ]
    messages.append({"role": "user", "content": transcript})
    
    return messages
