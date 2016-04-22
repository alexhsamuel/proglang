# 1. Date Calculator

A command line calculator for simple date expressions.

```sh
$ dc "2016-04-22 + 7"
2016-04-29
```

With `-c` or `--calendar`, the computation is performed in the given calendar.

```sh
$ dc -c weekdays "2016-04-22 + 7"
2016-05-03
```

The calendar is one of "all", "weekdays", "weekends", or the path to a calendar file.

The expression grammar is as follows:

- `DATE` := an ISO 8601 date
- `OFFSET` := a signed integer offset in days
- `DATE-EXPR` := `DATE-EXPR + OFFSET` | `DATE-EXPR - OFFSET` 
- `DATE-DIFF` := `DATE-EXPR - DATE-EXPR`
- `DATE-RANGE` := `DATE-EXPR .. DATE-EXPR` | `DATE-EXPR ... DATE-EXPR`
- `EXPR` := `DATE-EXPR` | `DATE-DIFF` | `DATE-RANGE`

The output is a single date, or an offset, or a sequence of dates, one per line.


# 2. Note Service

A REST service for short text notes, with user authentication.

A note has a (UTF-8) title, (UTF-8) text, an an internal ID assigned by the API.

Endpoints:

- `POST /oauth/token` - performs OAUTH2, returns an access token for other endpoints
- `POST /notes` - creates a new note
- `GET /notes/ID` - retrieves a note
- `PUT /notes/ID` - replaces an existing note
- `GET /notes` - returns a list of all note IDs and titles
- `GET /notes?s=TERM` - returns a list of all note IDs and titles matching TERM

The service is backed by a persistent database of some sort. Account credentials are retrieved from the database.
