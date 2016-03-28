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
GET /api/citation/mag/?type=author&id=<author_id>&publin_callback_url=<publin_url>
```

This call requests SCF. After the task is done, SCF sends the data in [SCF-JSON](api.md) format to the given callback URL. The sending is done by a POST request to `<publin_callback_url>?p=submit&m=bulkimportapi` with the content
```json
{
    'input': <data>
}
```

### Publin URL/data import (method 2)

Request the endpoint `/api/citation/mag/?type=author&id=<author_id>`, which returns an ID. This ID is the task ID and can be used to request the result at `/api/citation/mag/<task_id>/`. If the task is still running or failed, the meta information of the task will be returned instead. The meta information include among others the current status and when it failed the traceback error message
.

In Publin open the page `/?p=submit&m=bulkimport` and copy and paste the result URL into the input field. Alternative you can manually copy and the past the content from the result URL into the field.