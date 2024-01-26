# Fast API challenge
A code challenge to test and discuss about Fast API. If you randomly found out this repository, this is a challenge that me and my collegues from our study group created so we can practice and discuss Fast API

## The challenge

We will build an API where we can register and search places

### Register places

An endpoint must be exposed to allow new places to be registered. The places must be persisted to the database.

```
URL: /places
HTTP_METHOD: POST
SUCCESS_RESPONSE_CODE: 201
```

A place have the fields name, description and location. The request body must follow the JSON contract below

```
{
    "name": "string"
    "description": "string"
    "location": {
        "latitude": float,
        "longitude": float,
    }
}
```

Errors like invalid payloads must be treated and appropiate status code and error messages returned. No response body is required.

### Search places

An endpoint must be exposed to allow places to be search. The places can be filtered by name and location

```
URL: /places
HTTP_METHOD: GET
SUCCESS_RESPONSE_CODE: 200
```

The response must be paginated with [offset-pagination](https://developer.box.com/guides/api-calls/pagination/offset-based/) strategy. Feel free to decide the response body schema, the only requirement is that the places must follow the schema below:

```
{
    "name": "string"
    "description": "string"
    "location": {
        "latitude": float,
        "longitude": float,
    }
}
```

#### The search options

##### Name filtering

PlFor name filtering, a fulltext search style must be implemented. The name query string must be included in the URL like in snippet above

```
/places?name=value
```

##### Location filtering

 For location filtering, latitude, longitude and radius query string must be used together. Only places within the radius requested must be returned.

 ```
/places?latitude=40.15&longitude=50.15&radius=500
```

### Authentication

An API Key authentication must be implemented for all endpoints. The endpoint must expect the API Key to be present in the request headers in the format below

```
API-KEY: SomeValue
```

To simplify things, you can configure a fixed API KEY value as an envinronment variable

### Database

Feel free to use postgres or mongo as your datastore

### Code Design

Feel free to use the patterns and code architecture you believe is ideal for a production project

### Testing

The solution must be covered with automated tests

### [optional] Running

everything must be run inside a docker container
