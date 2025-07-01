import numpy as np
import random

from apo_metrics import compute_acc, lookup_score
from prompts import get_annotator_prompt_c012, get_annotator_prompt_c3456, get_annotator_prompt_c7
from llmclient import get_llm_response


def construct_full_subset(dataset):
    """dataset is a transcript (dataset[i])"""
    new_data = []
    rolling_history = ""
    for t in dataset["Transcript"]:
        for playa in ["P1", "P2"]:
            if playa in t:
                # Do stuff
                dialogue = t[playa]
                pro = f"{rolling_history}\nCURRENT: {dialogue}"
                scores = lookup_score(t["Turn"], playa, dataset)
                new_data.append({"Entry": pro, 
                                 "Scores": scores,
                                 "Turn": t["Turn"]})
                rolling_history += f"{playa}: {dialogue}\n"
    return new_data


def parse_and_collect_collection_apo(batch: list, originals: list, version: str, llm):
    """
    Slight variation on `parse_and_collect` for backwards compatibility with the APO code.
    This one is for the actual testing, not the APO algorithm itself. I know, confusing. But only one
    is exposed in the main code so it evens it out?
    (I wrote this one before the other)
    ---
    Params:
    batch: a list of prompts
    originals: a list of integers for every index in the batch
    version: the prompt version
    llm: the LLMClient
    """

    def fresh():
        response = {"Argument": None}
        crits = {f"C-{j}": np.nan for j in range(7)}
        response = dict(response, **crits)
        crits = {f"C-{j}_reason": np.nan for j in range(7)}
        response = dict(response, **crits)
        response["Winner"] = None
        response["Winner_reason"] = ""
        return response

    responses = []
    for b in batch:
        response = get_llm_response(llm, b)
        responses.append(response)

    all_parsed_responses = []
    for ix, (_resp, original) in enumerate(zip(responses, originals)):
        response = fresh()
        if version != "7":
            for k, v in original.items():
                response[k] = v
        if version != "7": #if ix < len(originals) - 1:
            resp = _resp.split("C-0")[0].strip()
            response["Argument"] = resp.replace("Argument:", "").strip()
            resp = _resp.split("C-")
            for r in resp[1:]:
                try:
                    _r, _reason = r.split("Reason:")
                except:
                    _r = r
                num = _r.split("C-")[-1][0]
                if _r.split(":")[-1].strip() == "N/A":
                    response[f"C-{num}"] = np.nan
                else:
                    try:
                        response[f"C-{num}"] = int(_r.split(":")[-1].strip().split(" ")[0].strip())
                    except:
                        response[f"C-{num}"] = np.nan
                try:
                    response[f"C-{num}_reason"] = _reason.strip()
                except:
                    response[f"C-{num}_reason"] = None
        else:
            resp = _resp.split("\n")
            winner = resp[0].replace("Winner:", "").strip()
            if "p2" in winner.lower():
                winner = "p2"
            elif "p1" in winner.lower():
                winner = "P1"
            elif "draw" in winner.lower():
                winner = "draw"
            try:
                reason = resp[1].replace("Reason:", "").strip()
            except:
                reason = None
            response["Winner"] = winner.strip()
            response["Winner_reason"] = reason

        all_parsed_responses.append(response)

    return all_parsed_responses



def parse_and_collect_apo(batch, originals, version, llm, debug=False):
    """
    Slight variation on `parse_and_collect` for backwards compatibility with the APO code.
    This one is for the APO algorithm itself. 
    ---
    Params:
    batch: a list of prompts
    originals: a list of integers for every index in the batch
    version: the prompt version
    llm: the LLMClient
    """

    def fresh():
        response = {"Argument": None}
        crits = {f"C-{j}": np.nan for j in range(7)}
        response = dict(response, **crits)
        crits = {f"C-{j}_reason": np.nan for j in range(7)}
        response = dict(response, **crits)
        crits = {f"C-{j}_raw": np.nan for j in range(7)}
        response = dict(response, **crits)
        response["Winner"] = None
        response["Winner_reason"] = ""
        response["Winner_raw"] = ""
        return response

    responses = []
    for b in batch:
        response = get_llm_response(llm, b)
        responses.append(response)

    all_parsed_responses = []
    for ix, (_resp, original) in enumerate(zip(responses, originals)):
        response = fresh()
        if _resp == "":
            raise "you need to increase tokens!"

        if version != "7": #if ix < len(originals) - 1:
            resp = _resp.split("C-0")[0].strip()
            response["Argument"] = resp.replace("Argument:", "").strip()
            resp = _resp.split("C-")
            for r in resp[1:]:
                try:
                    _r, _reason = r.split("Reason:")
                except:
                    _r = r
                num = _r.split("C-")[-1][0]
                if _r.split(":")[-1].strip() == "N/A":
                    response[f"C-{num}"] = np.nan
                else:
                    try:
                        response[f"C-{num}"] = int(_r.split(":")[-1].strip().split(" ")[0].strip())
                    except:
                        response[f"C-{num}"] = np.nan
                try:
                    response[f"C-{num}_reason"] = _reason.strip()
                except:
                    response[f"C-{num}_reason"] = None
        else:
            resp = _resp.split("\n")
            winner = resp[0].replace("Winner:", "").strip()
            if "p2" in winner.lower():
                winner = "p2"
            elif "p1" in winner.lower():
                winner = "P1"
            elif "draw" in winner.lower():
                winner = "draw"

            try:
                reason = resp[1].replace("Reason:", "").strip()
            except:
                reason = None
            response["Winner"] = winner.strip()
            response["Winner_reason"] = reason
            response["Winner_raw"] = original

        all_parsed_responses.append(response)

    return all_parsed_responses


def get_predictions_for_version_apo(subset: list, version: str, llm, prompt_override=None):
    """
    APO-only version of the loop calling prompts and getting responses.
    ---
    Params:
    subset: a list of [{entry, scores}] for a given subset of the transcript 
    version: the prompt version
    llm: the LLMClient
    prompt_override: whether we use a different system prompt: None or a str otherwise
    """
    rolling_history = ""
    batch = []
    scores = []
    for t in subset:
        pro, score = t["Entry"], t["Scores"]
        if version in "012":
            prompt = get_annotator_prompt_c012(pro, version, False, override=prompt_override)
        if version in "3456":
            prompt = get_annotator_prompt_c3456(pro, version, False, override=prompt_override)
        # We need the full transcript, not the turn-by-turn rolling history
        if version == "7":
            prompt = get_annotator_prompt_c7(pro, "7", False, override=prompt_override)
        batch.append(prompt)
        scores.append(score)

    responses = parse_and_collect_apo(batch, [i for i in range(len(batch))], version, llm)
    return scores, responses, subset


def get_predictions_for_version_collection_apo(subset, version, llm, prompt_override=None, developer=False):
    """
    The loop calling prompts and getting responses for testing (not APO algorithm itself)
    ---
    Params:
    subset: a list of [{entry, scores}] for a given subset of the transcript 
    version: the prompt version
    llm: the LLMClient
    prompt_override (None): whether we use a different system prompt: None or a str otherwise
    developer (False): whether this uses the "developer" or the "system" key in the call. Defaults to False
    """
    rolling_history = ""
    batch, originals = [], []
    squashed = []
    for t in subset["Transcript"]:
        squash = {"Turn": t["Turn"]}
        for p in ["P1", "P2"]:
            if p in t:
                dialogue = t[p]
                squash[p] = dialogue
                pro = f"{rolling_history}\nCURRENT: {dialogue}"
                if version in "012":
                    prompt = get_annotator_prompt_c012(pro, version, False, override=prompt_override, developer=developer)
                if version in "3456":
                    prompt = get_annotator_prompt_c3456(pro, version, False, override=prompt_override,  developer=developer)
                # We need the full transcript, not the turn-by-turn rolling history
                if version == "7":
                    prompt = get_annotator_prompt_c7(pro, "7", False, override=prompt_override, developer=developer)
                rolling_history += f"{p}: {dialogue}\n"
                batch.append(prompt)
                originals.append({
                    "Turn": t["Turn"],
                    p: t[p],})
        squashed.append(squash)
    responses = parse_and_collect_collection_apo(batch, [i for i in range(len(batch))], version, llm)
    if version != "7":
        for s in squashed:
            for p in ["P1", "P2"]:
                if p in s:
                    matches = [m for m in responses if m["Turn"] == s["Turn"] and p in m and m[p] == s[p]][0]
                    s[f"{p}Scores"] = {
                        f"C-{version}": matches[f"C-{version}"],
                        f"C-{version}_reason": matches[f"C-{version}_reason"],
                        "Argument": matches["Argument"],
                    }
        return squashed
    else:
        return responses[-1]


def apo(initial_prompt: str, dataset: list, version: str, llm, beam_width=4, search_depth=6, max_token_override: dict =None, debug: bool =False):
    """
    Main loop for the APO algorithm. All are the defaults from the original paper.
    ---
    Params:
    initial_prompt: str: the initial prompt on which to run APO
    dataset: list of entries compatible with `get_predictions_for_version_apo`
    version: prompt version (i.e., one of "01234567")
    llm: the LLMClient object
    beam_width: ...the width of the beam? Defaults to 4
    search_depth: int to determine the depth (loops) at which you will run APO.
    max_token_override: dict of the form {"tkey": tkey, "max_tokens": max_tokens to override}. You need both because some LLMs use different token keys.
    debug: debug.
    """    
    b0 = [(initial_prompt, 0)]
    for i in range(search_depth):
        candidates = []
        # Our train set is 4k -- model will only see 64.
        subset = random.sample(dataset, k=64)
        if debug: print(f"b0: {b0}")
        for prompts, scores in b0:
            candidates += expand(prompts, subset, version, llm, max_token_override=max_token_override, debug=debug)
        # Sampling to avoid overrun
        _cands = random.sample(candidates, k=8) if len(candidates) > 8 else candidates
        if debug: print(f"chosen candidates {_cands}")
        if _cands != []:
            b0 += select(_cands, dataset, version, llm, beam_width)
        if debug: break
    b0.sort(key=lambda x: x[-1], reverse=True)
    return b0


def expand(p_candidate: list, subset: list, version: str, llm, max_token_override=None, max_errors=4, debug=False):
    """
    Beam search proper.
    ---
    Params:
    p_candidate: a list of candidate prompts
    subset: the list of entries compatible with `get_predictions_for_version_apo` (i.e., the dataset)
    version: the prompt version
    llm: the LLMClient object
    max_errors: the maximum number of mismatched datapoints allowable to run for the gradient version
    max_token_override: dict of the form {"tkey": tkey, "max_tokens": max_tokens to override}. You need both because some LLMs use different token keys.
    debug: gee I wonder what this does.
    """
    if debug: print("Calling for predictions")
    scores, resps, entries = get_predictions_for_version_apo(subset, version, llm, prompt_override=p_candidate)
    errors = []
    accuracy = compute_acc(resps, scores, version)
    if debug: print(f"Called {len(subset)} predictions and got accuracy {accuracy}")
    for entry, resp, score in zip(entries, resps, scores):
        if version == "7":
            p, s = resp["Winner"], s = score["Winner"]
            p, s = p.lower(), s.lower()
        else:
            p = resp[f"C-{version}"]
            s = score[f"C-{version}"]
            if np.isnan(p):
                p = "N/A"
            else:
                p = int(p)
        if p != s:
            errors.append(entry)
    errors = random.sample(errors, k=min(len(errors), max_errors))
    # Minor hack (not in the paper): if no errors, we've converged
    if debug: print(f"Selected {len(errors)}")
    if errors == []:
        successors = [p_candidate]
    else:
        successors = gradient_and_edit(p_candidate, errors, version, llm, max_token_override=max_token_override, debug=debug)
    return successors


def gradient_and_edit(p_candidate: list, errors: list, version: str, llm, max_token_override=None, num_reasons=4, 
                      edits_per_gradient=1, num_mc_samples=2, debug=False):
    """
    Run the pseudo gradient.
    All params and prompts are the defaults from the paper.
    ---
    Params:
    p_candidate: a list of candidate prompts
    errors: a list of entries where the label was wrong compatible with `get_predictions_for_version_apo` (i.e., the dataset)
    version: the prompt version
    llm: the LLMClient object
    max_token_override: dict of the form {"tkey": tkey, "max_tokens": max_tokens to override}. You need both because some LLMs use different token keys.
    num_reasons: number of reasons required for the LLM to output as to why this was wrong
    edits_per_gradient: number of edits done for the prompts that were wrong
    num_mc_samples: the samples for the Monte-Carlo bit
    debug: debug.
    """
    def gradient_prompt(p, e, f): 
        resp = [{"role": "user", "content": f"I'm trying to write a zero-shot classifier prompt.\nMy current prompt is:\n\"{p}\"\nBut this prompt gets the following examples wrong:\n{e}\ngive {f} reasons why the prompt could have gotten these examples wrong.\nWrap each reason with <START> and <END>"}]
        return resp

    def edition_prompt(p, e, g, n):
        resp = [{"role": "user", "content": f"I'm trying to write a zero-shot classifier.\n My current prompt is:\n\"{p}\"\nBut it gets the following examples wrong:\n{e}\nBased on these examples the problem with this prompt is that:\n{g}\nBased on the above information, I wrote {n} different improved prompts.\nEach prompt is wrapped with <START> and <END>.\nThe {n} new prompts are:"}]
        return resp
    
    def mc_prompt(p):
        resp = [{"role": "user", "content": f"Generate a variation of the following instruction while keeping the semantic meaning.\nInput: {p}\nOutput:"}]
        return resp

    old_tokens = llm._params["tokens"]
    tkey = [k for k in llm._params.keys() if "tokens" in k][0]
    if max_token_override is not None:
        tkey = max_token_override["tkey"]
        tokens = max_token_override["tokens"]
        llm.update_params({tkey: tokens})
    
    # Direct call to model, postprocess "gradient"
    if version != "7":
        error_string = "\n - ".join([p["Entry"] + ": " + str(p["Scores"][f"C-{version}"]) for p in errors])
    else:
        error_string = "\n - ".join([p["Entry"] + ": " + str(p["Scores"][f"Winner"]) for p in errors])
    prompt = gradient_prompt(p_candidate, error_string, str(num_reasons))
    if debug: print(f"Prompt is \n{prompt}\n for the gradient step")
    response = get_llm_response(llm, prompt)
    if debug: print(f"ot \n{response}\n from the gradient step")
    
    # Edit the prompt -- one edit per gradient.
    edited_prompts = []
    # Note: the original paper doesn't specify parsing. We need to keep it or else this algorithm won't work.
    response_processed = [r.replace("<END>", "").strip() for r in response.split("<START>") if "<END>" in r]
    for g in response_processed:
        prompt = edition_prompt(p_candidate, error_string, g.strip(), str(edits_per_gradient))
        response = get_llm_response(llm, prompt)
        edited_prompts.append(response.strip())
    # Do MC search
    # Two candidates per instruction:
    if debug: print(f"Here are the edited prompts:\n{edited_prompts}")
    candidates = []
    for c in edited_prompts:
        # I would like to make this a batch call but I don't want to alter the original work.
        for _ in range(num_mc_samples):
            response1 = get_llm_response(llm, mc_prompt(c))
            # Same as before: no parsing in paper
            response_processed = [r.replace("<END>", "").strip() for r in response1.split("<START>") if "<END>" in r]
            if response_processed != []:
                response1 = response_processed[0]
            candidates.append(response1)

    llm.update_params({tkey: old_tokens})
    return candidates


def select(candidates: list, dataset: list, version: str, llm, beam_size: int, B=12):
    """
    Select candidates.
    ---
    Params:
    candidates: a list of prompt candidates
    dataset: a list of entries compatible with `get_predictions_for_version_apo` (i.e., the dataset)
    version: the version for the prompt
    llm: the LLMClient object
    beam_size: the size of the beam
    """
    # Paper states that B in 12-50 keeps it steady.
    # This is a very confusing and not-very-well-written algorithm.
    # We'll implement it verbatim from the paper though.
    S = [(p, 0) for p in candidates]
    old_s = [s for s in S]

    def get_n(i, T):
        # What is T lmao 
        # From the below, our maximum number of iterations (n) cannot be larger than T
        # Likewise, B gets too degenerate when close to T (T < B, otherwise you'll just get zeroes)
        left = 1/(0.5*sum([1/j for j in range(2, T + 1)]))
        right = (B-T)/(T + 1 - i)
        return int(np.ceil(left*right))

    # Says 1... n - 1 for n prompts; index shift python
    m = min(len(candidates) - 2, beam_size + 1)
    for i in range(1, m):
        subset = random.sample(dataset, k=get_n(i, m))
        # Original paper isn't very clear here (i is not defined; We'll evaluate all prompts)
        S_exp = []
        for prompt, _ in S:
            scores, resps, _ = get_predictions_for_version_apo(subset, version, llm, prompt_override=prompt)
            accuracy = compute_acc(resps, scores, version)
            S_exp.append((prompt, accuracy))
        S_exp.sort(key = lambda x: x[-1], reverse=True) # Decreasing
        S = [p for p in S_exp[:-1]]
    # We also need to address this corner case, not addressed in the paper
    if S == []:
        S = old_s
    return [S[0]]

