import numpy as np
from prompts import get_annotator_prompt_c012, get_annotator_prompt_c3456, get_annotator_prompt_c7
import time
from llmclient import get_llm_response


def parse_and_collect(batch: list, originals: list, version: str, model: str, llm, debug=False):
    """
    Gather the responses (prompts) in batch. This code has a lot of legacy junk from using async APIs.

    Params:
    batch: the list of prompts: [prompt]
    originals: an index: [i for i in len(batch)]
    version: the prompt version to call
    model: the model key
    llm: the actual LLMClient instance
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

    if debug: print(f"Sending {batch}")
    responses = get_llm_response(llm, batch)
    if debug: print(f"Got: {responses}")
    responses = [responses]
    originals = [originals]

    all_parsed_responses = []
    for ix, (original_response, original) in enumerate(zip(responses, originals)):
        response = fresh()
        _resp = original_response
        if "deepseek" in model:
            # Deepseek doesn't exactly follow the instructions
            _resp = _resp.replace("-", "").replace("*", "")
            _resp = _resp.replace(f"C-{version},", "").replace(" (Conviction Level)", "")
            _resp = _resp.split("</think>")[-1].strip()
            if f"C-{version}:" not in _resp:
                _resp = _resp.replace(f"Label: C{version}", f"Label: C-{version}")
                _resp = _resp.replace(f"C{version}", f"C-{version}")
                _resp = _resp.replace("the label is ", f"C-{version}: ")
                _resp = _resp.replace("the label would be ", f"C-{version}: ")
                _resp = _resp.replace("C-{version} label is ", f"C-{version}: ")
        if version != "7": #if ix < len(originals) - 1:
            for k, v in original.items():
                response[k] = v
            response[f"C-{version}_raw"] = original_response
            resp = _resp.split(f"C-{version}")[0].strip()
            response["Argument"] = resp.replace("Argument:", "").strip()
            resp = _resp.split(f"C-{version}")
            try:
                r = resp[1]
                try:
                    _r, _reason = r.split("Reason:")
                except:
                    _r = r
                num = version
                if _r.split(":")[-1].strip() == "N/A":
                    response[f"C-{num}"] = np.nan
                else:
                    try:
                        response[f"C-{num}"] = int(_r.split(":")[1].strip().split(" ")[0].strip())
                    except:
                        response[f"C-{num}"] = np.nan
                try:
                    response[f"C-{num}_reason"] = _reason.strip()
                except:
                    response[f"C-{num}_reason"] = None
            except:
                response[f"C-{version}"] = np.nan
                response[f"C-{version}_reason"] = None
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
            response["Winner_raw"] = original_response

        all_parsed_responses.append(response)

    return all_parsed_responses


def get_predictions_for_version(subset: list, version: str, model: str, llm, prompt_override=None, developer=False, debug=False):
    """
    Get the predictions for a version. This automatically constructs the prompts.
    Params:

    subset: a subset of the dataset. That is basically a row of the dataframe
    version: a version ("0-7") of the prompt to be called. 
    model: the key that we will use to index the model under Annotations
    llm: the LLM client object
    prompt_override: any different system prompt you'd like to try
    developer: a bool in case you need to switch "system" for "developer"
    debug: log everything
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
                    prompt = get_annotator_prompt_c012(pro, version, False, override=prompt_override, developer=False)
                if version in "3456":
                    prompt = get_annotator_prompt_c3456(pro, version, False, override=prompt_override,  developer=False)
                # We need the full transcript, not the turn-by-turn rolling history
                if version == "7":
                    prompt = get_annotator_prompt_c7(pro, "7", False, developer=False)
                rolling_history += f"{p}: {dialogue}\n"
                batch.append(prompt)
                originals.append({
                    "Turn": t["Turn"],
                    p: t[p],})
        squashed.append(squash)
    responses = []
    if version == "7":
        batch = [batch[-1]]
        originals = [originals[-1]]
    for b, o in zip(batch, originals):
        response = parse_and_collect(b, o, version, model, llm, debug=debug)[0]
        responses.append(response)
    if version != "7":
        for s in squashed:
            for p in ["P1", "P2"]:
                if p in s:
                    matches = [m for m in responses if m["Turn"] == s["Turn"] and p in m and m[p] == s[p]][0]
                    s[f"{p}Scores"] = {
                        f"C-{version}": matches[f"C-{version}"],
                        f"C-{version}_reason": matches[f"C-{version}_reason"],
                        f"C-{version}_raw": matches[f"C-{version}_raw"],
                        "Argument": matches["Argument"],
                    }
        return squashed
    else:
        return responses[-1]
