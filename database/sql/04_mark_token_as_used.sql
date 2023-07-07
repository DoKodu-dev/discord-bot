update tokens
set
    used = True,
    used_by = ?,
    used_date = ?
where token ilike ?;