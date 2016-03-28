<h1>API</h1>

### SCF-JSON format

SCF exports publications and it's citing publication in the so called SCF-JSON format.

Example for a single publication
```json
{
    "type": "article",
    "title": "Example title",
    "booktitle": "A book title",
    "publisher": "Publisher press",
    "year": 1992,
    "volume": 23,
    "pages_from": 10,
    "pages_to": 3,
    "number": 1,
    "series": "Example series",
    "abstract": "This paper is about the XX",
    "copyright": "Copyright by example.org",
    "journal_name": "Journal of Example",
    "url": "http://example.org",
    "doi": "21614",
    "isbn": "000-0-00-000000-0",
    "authors": ["Tom Müller", "Miri Schneider"],
    "keywords": ["awesome", "great"]
}
```

Multiple publications are represented as array
```
[
  { <publication> },
  { <another publication> }
]
```

Example for a publication with citations
```
{
    "type": "article",
    "title": "Example Title",
    "journal_name": "Journal of Example",
    "year": 2015,
    "authors": ["Miri Müller"],
    "citations": [
        {
            "type": "article",
            "title": "This paper cites Example Title",
            "journal_name": "Journal A",
            "year": 2016,
            "authors": ["Miri Müller"]
        },
        {
            "type": "article",
            "title": "And this paper too",
            "journal_name": "Journal A",
            "year": 2016,
            "authors": ["Tom Müller"]
        }
    ]
}
```

### Find citations - parameters

|Parameter|Type|Required|Description|
|---------|----|--------|-----------|
|`type`|'author', 'journal'|yes|Query type|
|`id`|int|id or name required|ID|
|`name`|string|id or name required|Name|
|`publin_callback_url`|URL|no|Callback URL|
|`fieldofstudy`|'isi'|no|ISI field of study|