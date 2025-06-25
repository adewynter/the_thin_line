from transformers import pipeline
#transformers.logging.set_verbosity_error()


def get_llm_response(model, assembled_prompt, debug=False):
    try:
        resp = model.send_request(assembled_prompt)
    except:
        return "FAIL"
    if type(assembled_prompt) == list:
        return resp[0]["generated_text"][-1]["content"]
    return resp[0]["generated_text"][len(assembled_prompt):]


class LLMClient():
    """
    Client to run SLM code available in Huggingface.
    For OpenAI code, you should update this class to work with their API.
    """
    def __init__(self, params, model_id, is_dumb=False):
        self._pipeline = pipeline(
            "text-generation",
            model=model_id,
            device_map="auto",
        )
        # OpenAI's temperature range is [0,2] for some  reason.
        # For backwards compat with the GPT-*/o* code, we halve it if it is not dumb.
        self._is_dumb = is_dumb 
        self._params = params
        self._model = model_id

    def send_request(self, assembled_prompt):
        #eos_token_id=terminators
        outputs = self._pipeline(assembled_prompt, 
                           temperature=self._params["temperature"] if self._is_dumb else self._params["temperature"]/2, 
                           max_new_tokens=self._params["max_tokens"],
                           pad_token_id = self._pipeline.tokenizer.eos_token_id)
        return outputs

    def update_params(self, params):
        for k, v in params.items():
            self._params[k] = v
