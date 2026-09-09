# Verified robots.txt user-agent tokens (2026-09-09)

Primary sources only. No blog secondary lists.

| Token | Source |
| --- | --- |
| GPTBot | https://platform.openai.com/docs/bots |
| OAI-SearchBot | https://platform.openai.com/docs/bots |
| ChatGPT-User | https://platform.openai.com/docs/bots |
| PerplexityBot | https://docs.perplexity.ai/docs/resources/perplexity-crawlers |
| Perplexity-User | https://docs.perplexity.ai/docs/resources/perplexity-crawlers |
| ClaudeBot | https://support.anthropic.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler |
| Claude-SearchBot | same Anthropic article |
| Claude-User | same Anthropic article (official third Anthropic bot; included with Claude-SearchBot) |
| Google-Extended | https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers |
| Googlebot | Google crawling docs (search indexing; separate from Google-Extended) |
| bingbot | Microsoft Bing crawler token (UA contains bingbot/2.0; +http://www.bing.com/bingbot.htm) |
| Applebot | https://support.apple.com/en-us/119829 |
| Applebot-Extended | https://support.apple.com/en-us/119829 |

Notes:
- Google-Extended and Applebot-Extended are product/control tokens in robots.txt; they may not send a distinct HTTP User-Agent string.
- ChatGPT-User and Perplexity-User are often user-initiated; providers note robots.txt may not always apply. Still listed Allow for clarity.
- No llms.txt. Evidence does not support it.
