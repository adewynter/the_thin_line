# The Thin Line

Repository for the paper [The Thin Line Between Comprehension and Persuasion in LLMs](https://arxiv.org/abs/2507.01936), by Adrian de Wynter and Tangming Yuan. 

In this work we show that LLMs are _excellent_ debaters. They are persuasive, logical, and coherent. 
We _also_ show that they are very poor evaluators of the same dialogue, with inconsistent results and low agreement with human-based annotations. 

We also find that disclosing AI (or suspecting AI) allows people to be far more critical of the arguments that AI makes. Overall, debating with AI was shown to be both persuasive and a good tool for self-reflection, which in turn suggests that this structure be useful when the use of AI is disclosed.

Our conclusion is two-fold:
1. **LLMs do _not_ understand** the task, the dialogue, and they are **inconsistent reasoners**
2. However, given their effectiveness, we also conclude that **you do not need to understand in order to persuade**.

That said, given (1), (2) can be rephrased as:

>If an agent is able to convincingly maintain a dialogue, **does it matter that it cannot show that it knows what it is talking about?**

In other words, from the perspective of argumentation theory, do we _really_ need to model pragmatic context and coherence of arguments?

## Repo
This repository contains all the code and data used in our work. It is not just for reproducibility purposes: we would like to see what you can do with it! 
Here's what the repo contains:

| Folder | Description |
| --- | --- |
| `processed_transcripts` | Transcripts of the debates, annotated. It also includes the APO prompts |
| `audio_transcripts` | Transcripts (text-to-speech) of the debates |
| `audio_annotations` | Annotations for the transcripts |

All data can be evaluated with the `Evaluator.ipynb` notebook. The rest of the Python files are for readability (because nobody likes spaghetti code).

## Citation
If you find our paper useful in your work, please consider citing our paper:

```
@misc{dewynter2025linecomprehensionpersuasionllms,
      title={The Thin Line Between Comprehension and Persuasion in {LLMs}}, 
      author={Adrian de Wynter and Tangming Yuan},
      year={2025},
      eprint={2507.01936},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2507.01936}, 
}
``` 

## Licence

MIT