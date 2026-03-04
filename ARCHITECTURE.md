Stages
- [ ] Planning (Current)
- [ ] Environment

## Preambles
Some significance is placed on developer market share, because it directly influences the ecosystem support and the number of developers who would be able to support the development effort.

Performance is likely not an issue considering that compute will likely be minimal and operations will be I/O bound. However, this is merely an educated guess and testing should be done to see if there are parts that can be significantly sped up by abstracting the logic into native language modules through either native modules (via Maturin), or more likely, a Rust microservice. Rust development is expensive, so this will be used in light sprinkles in necessary situations. And it is essentially never going to occur.

# Architecture

## Frontend
### Framework
React is far and away the most well used frontend:
 - It is sufficiently performant
 - It has a huge ecosystem of libraries
 - The market for software developers that know React is huge, making it easier to find someone to maintain

Angular and Vue are very competent alternatives as well, but:
 - I am not familiar as familiar with Vue as I am with React. And I have not touched on Angular before. I can definitely familiarise myself with both of them, but there are no immediate reasons that I can think of that would make React unsuitable
 - They both have significantly lower market share of developers

I don't think we should use SSR, however, because:
 - Both the frontend we are building and the frontends that could be written by other developers would likely be internal (really?) so SEO is not a problem at all
 - The brunt of the logic will be on the backend, it is best that we keep it as simple as possible.
 - Having tried using SSR before on my portfolio site, there are some "gotchas" when it comes to hydration. While it is not difficult to solve, this will be a point of consideration when writing any client-side component, for no good benefits in return.

| Candidates            | Bundler                                                         | Developers                                           |
|-----------------------|-----------------------------------------------------------------|------------------------------------------------------|
| Next                  | Turbopack is more performant but only recently production-ready | Most used framework (21.5%)                          |
| Vite                  | Vite's bundler is fast and well-tested                          | Very well-used. Beloved by many for its performance. |
| WIP, researching more |                                                                 |                                                      |

Because of our target audience: people who are more interested with getting the job done with the data:
 - It will be prudent not to try anything too flashy and distracting. _**Definitely** not going to be designed with the same theme as my portfolio page._
 - For clarity of data and stats, ensure good contrast and readabiity
 - However, we should not pessimise the design, we should make sure it is not an eyesore.
 - Should be intuitive to the users. My current assumption is that they would be familiar with Microsoft Office. I think it will be nice to be able to do a mockup, and to speak to some of the people who would be the _end users_ using the app to see what they would be interested in, and gather some user feedback about things that we are planning to do, to make sure that our thoughts are aligned well with the end-user.

### UI library
There are a lot of UI libraries out there, for our purposes, I don't think we should be too hung up on this choice. Most of them are sufficient for our use case of a simple interface. I think our time would be better spent thinking about the product itself.

However, I would prefer not to use libraries that forces us to use Tailwind, like shadcn:
 - I found that it discourages _me_ from following best practices --- separating the styling of components and their layout
 - If we have custom CSS atop of it, you may need to go back and forth between the layout and style files, and it will be confusing to other developers.
 - In fact, I am looking towards removing it from my portfolio site.

## Backend
| Candidates        | General                                                                                                                                                                                                                                            | Language                                                                          | Ecosystem for Postgres                                        | OpenAPI support |
|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|---------------------------------------------------------------|-----------------|
| Express (Node.js) | Simple, sufficiently performant, well-used (20.3%, highest framework on SO dev survey).                                                                                                                                                            | TypeScript, well-used, easy to write, very good type system.                      | Slonik for SQL templating and connecting to the sql instances | Through swagger |
| Fastify (Node.js) | More performant than Express, more batteries included, well-used but less commonly known (3.1%) <br><br> Developers' sentiment seems to prefer Fastify because it's more modern and more performant, albeit, from what I have read, marginally so. | TypeScript                                                                        | Same as above                                                 | Yes             |
| FastAPI (Python)  | Simple, also performant, well-used (15.1%)                                                                                                                                                                                                         | Python, _most well known language_, especially amongst data users, easy to write. | Psycopg + Jinja for templating                                | Yes             |

 - It may be prudent to use JSON Schema for standardization. This will allow us, as well as other developers to parse the data easily together with the correct types
 - Depending on the language that the team prefers to use, Python + FastAPI may be the more prudent choice
 - A greenfield project like this has the opportunity to adopt the more modern Fastify
 - Express is so-called "battle-tested", there are significant resources available for Express and developer market share is highest for Express

One of the challenge that I can think of: While it is not directly linked to the backend, when initially importing this data to the Postgres instances, we might encounter database locking issue if multiple data owners are trying to upload large amount of data at the same time.
 - I am looking at ways to mitigate this, it will be prudent to run a stress test internally to inform if the implementation is sound and viable.
 - We should not assume that this only happens when initially populating the data, some data owners may upload a large batch of data at once, and we will need to ensure that we have a plan to deal with this. Depending on the scenario, it might not be prudent to simply send a "413 Content Too Large" error, because it could cause irreversible data loss. If we choose to do so, and this will likely be the case at the start of development, we should ensure that limits are well documented together with the API endpoint in question.

I have heard about the OpenAPI standard in online forums and someone mentioned to me that I should look it up.

I am going to investigate if it is doable to generate OpenAPI documentation, I think it will be prudent for us to do so. Sticking to the industry standards will prove worthwhile for both people who are trying to access this API, and to find people to maintain it in the future.

## API Documentation
At the beginning, we can use a static site generator that takes markdown files. For ease of documentation during development.

Because the API documentation is expected to be mostly static, there is no need for us to be using a dynamic site. Definitely no backend for this (except for connecting to the backend for testing)

| Candidates | Remarks                                                                                                                                                                                                                                                            |
|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Next       | As much as I like Next.js, there's no denying that it's static site support is only an afterthought, however, I think it is competent enough, from what I have seen<br> - Using Next may reduce the mental load for development. We'll have to see if this is true |
| Astro      | Much leaner approach, purpose-built for static sites. I am interested in giving this a try. It is well-used for documentation sites. I have not used it, but I have heard praises about it. I might try this in my own time.                                       |

## Load balancing, Spam and DDoS protection, and other reverse proxy services
Likely already handled by other microservices? More information is needed.

## Information gaps
What I currently need to investigate:
 - Kubernetes environment for testing, which is as close as I can get to OpenShift considering I don't have the node to run it myself, this will be set up on this repo.
    - I will investigate, install and set up Minikube + Kubectl
    - I will create very simple test apps for the frontend and backend to ensure that everything is calling each other properly
    - The frontend, backend and documentation services will be pulled in as dependencies
 - ~~Statically generated documentation site, with ability to pull in API definitions from the backend codebase to generate code samples~~
    - ~~Also includes testing the code samples during build~~
    - While this will be good to do, I think it will be more prudent to leave this as a potential continuous improvement idea, rather than part of an MVP. Moved to [future ideas](#potential-ideas-for-the-future)
 - WIP


# MVP targets
## Architecture
WIP

## User flow
| Data owner                                                                                                                                                | Admin                                    | Data user                                                                                                                          |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
|                                                                                                                                                           | Able to view and edit perms              |                                                                                                                                    |
| Login as data owner<br> - This demonstrates the ability to authenticate with OAuth                                                                        | Login as admin                           | Login via data user                                                                                                                |
| Subscribe to data                                                                                                                                         | Subscribe to data                        | Subscribe to data                                                                                                                  |
| Receive a sample dataset that consists of some persons' data in json format and some images<br> - This demonstrates the abiity to ingress multimodal data |                                          |                                                                                                                                    |
| Pick out relevant data, which as a side-effect, also removes [PHIs](https://ohdsi.github.io/CommonDataModel/cdmPrivacy.html)                              |                                          |                                                                                                                                    |
| Data is formatted into OMOP schema and written into database                                                                                              |                                          |                                                                                                                                    |
| Ingressed data is displayed<br> - This demonstrates pubsub                                                                                                | Ingressed data is displayed              | Ingressed data that they have access to is displayed<br><br> Ingressed data they don't have access to is queried, accessed or sent |
| Able to review history of ingressed data                                                                                                                  | Able to review history of ingressed data |                                                                                                                                    |

## Potential ideas for the future
 - Python client library for accessing the API
 - Statically generated documentation site, with ability to pull in API definitions from the backend codebase to generate code samples
    - Also includes testing the code samples during build. I really enjoy Neon's documentation (https://github.com/neondatabase) for its convenience. Individual API endpoints have sample code which makes it very easy for people to get started and develop. I think it will be interesting to try building something like this _in the future_. For code samples, target curl, JS's fetch API and Python's requests, because these are the most commonly used and the most basic. Because the API documentation is expected to be mostly static, there is no need for us to be using a dynamic site. Definitely no backend for this (except for connecting to the backend for testing)
    - Reason being: I really enjoy Neon's documentation (https://github.com/neondatabase) for its convenience. Individual API endpoints have sample code which makes it very easy for people to get started and develop. I think it will be interesting to try building something like this _in the future_. For code samples, target curl, JS's fetch API and Python's requests, because these are the most commonly used and the most basic.
