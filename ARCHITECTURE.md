Stages
- [ ] Planning (Current)
- [ ] Environment

## Preambles
A lot of significance is placed on developer market share, because it directly influences the ecosystem support and the number of developers who would be able to support the development effort.

Performance is likely not an issue considering that compute will likely be minimal. However, this is merely an educated guess and testing should be done to see if there are parts that can be significantly sped up by abstracting the logic into native language modules through either native modules (via Maturin), or more likely, a Rust microservice.

Rust development is expensive, so this will be used in light sprinkles in necessary situations. And it is unlikely going to occur.

# Architecture

## Frontend
React is far and away the most well used frontend
There is no reason to use SSR
| Candidates | Bundler                                                         | Developers                                           |
|------------|-----------------------------------------------------------------|------------------------------------------------------|
| Next       | Turbopack is more performant but only recently production-ready | Most used framework (21.5%)                          |
| Vite       | Vite's bundler is fast and well-tested                          | Very well-used. Beloved by many for its performance. |

Obviously nothing flashy, no blinking distractions, good contrast and readabiity, yet not an eyesore. _**Definitely** not going to be designed with the same theme as my portfolio page._

Should be intuitive to the users. Which I am going to assume, are familiar with Microsoft Office.

From my understanding, the target audience will included people who are not tech-savvy, in which case, I would like to iterate and "playtest" with some of the users to see if they know what to do.

## Backend
| Candidates        | General                                                                                                                                                                         | Language                                                                                                                                                                  | Ecosystem                                                     | OpenAPI support |
|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------|-----------------|
| Express (Node.js) | Simple, sufficiently performant, well-used (20.3%, highest framework on SO dev survey)                                                                                          | TypeScript, well-used, easy to write, very good type system. <br><br> This type system can be declared on DefinitelyTyped for better developer experience on the frontend | Slonik for SQL templating and connecting to the sql instances | Through swagger |
| Fastify (Node.js) | More performant than Express, more batteries included, well-used but less commonly known (3.1%) <br><br> Developers' sentiment seems to prefer Fastify because it's more modern | TypeScript                                                                                                                                                                | Same as above                                                 | Yes             |
| FastAPI (Python)  | Simple, also performant, well-used (15.1%)                                                                                                                                      | Python, _most well known language_, especially amongst researchers and clinicians , easy to write.                                                                        | Psycopg + Jinja for templating                                | Yes             |

Same safe approach to APIs as to the frontend.

It is probably best to generate OpenAPI as we go. Sticking to the industry standards will prove worthwhile for both people who are trying to access this API, and to find people to maintain it in the future.

## API Documentation
I really enjoy Neon's documentation (https://github.com/neondatabase) for it's usability and convenience to users.

Individual API endpoints have sample code which makes it very easy for people to get started and develop.

For code samples, target curl, JS's fetch API and Python's requests, because these are the most commonly used and the most basic.

Because the API documentation is expected to be mostly static, there is no need for us to be using a dynamic site. Definitely no backend for this (except for connecting to the backend for testing)

| Candidates | Remarks                                                                                                                               |
|------------|---------------------------------------------------------------------------------------------------------------------------------------|
| Next       | As much as I like Next.js, there's no denying that it's static site support is only an afterthought, however, I think it is competent |
| Astro      | Much leaner approach, purpose-built for static sites                                                                                  |

## Load balancing, Spam and DDoS protection, and other reverse proxy services
Likely already handled by other microservices? More information is needed.

## Information gaps
What I currently need to investigate:
 - Kubernetes environment for testing, which is as close as I can get to OpenShift considering I don't have the node to run it myself, this will be set up on this repo.
    - I will investigate, install and set up Minikube + Kubectl
    - I will create very simple test apps for the frontend and backend to ensure that everything is calling each other properly
    - The frontend, backend and documentation services will be pulled in as dependencies
 - Statically generated documentation site, with ability to pull in API definitions from the backend codebase to generate code samples
    - Also includes testing the code samples during build
 - WIP