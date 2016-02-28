<h1>Integration</h1>

## Publin


### Publin callback (method 1)

Publin does not support authentication via URL yet. Hence you have to deactivate it by comment out the following lines in `src/Submitcontroller.php`
```php
if (!$this->auth->checkPermission(Auth::SUBMIT_PUBLICATION)) {
	throw new PermissionRequiredException(Auth::SUBMIT_PUBLICATION);
}
```

For Publin the parameter `publin_callback_url` is used, which should be the base URL (e.g. http://example.org/publin/) to the Publin instance.

```bash
/api/citation/mag/?author_id=<author_id>&publin_callback_url=<publin url>
```

This call requests SCF. After the task is done, SCF sends the data in [SCF-JSON](api.md) format to the given callback URL. The sending is done by a POST request to `<publin_callback_url>?p=submit&m=bulkimportapi` with the content
```json
{
    'input': <data>
}
```

### Publin URL import (method 2)

Request `/api/citation/mag/?author_id=<author_id>`, which returns an ID. This ID is the task id and can be used to request the result at `/api/citation/mag/<task_id>/`.

In Publin open the page `/?p=submit&m=bulkimport` and copy and paste the result URL into the input field.