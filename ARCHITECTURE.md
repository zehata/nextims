Stages
- [ ] Planning (Current)
- [ ] Environment

## Preambles
A lot of significance is placed on developer market share, because it directly influences the ecosystem support and the number of developers who would be able to support the development effort.

Performance is likely not an issue considering that compute will likely be minimal. However, this is merely an educated guess and testing should be done to see if there are parts that can be significantly sped up by abstracting the logic into native language modules through either native modules (via Maturin), or more likely, a Rust microservice.

Rust development is expensive, so this will be used in light sprinkles in necessary situations. And it is unlikely going to occur.

# Architecture

## Frontend
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
 - WIP


| Candidates | Bundler                                                         | Developers                                           |
|------------|-----------------------------------------------------------------|------------------------------------------------------|
| Next       | Turbopack is more performant but only recently production-ready | Most used framework (21.5%)                          |
| Vite       | Vite's bundler is fast and well-tested                          | Very well-used. Beloved by many for its performance. |

Because of our target audience: people who are more interested with getting the job done with the data:
 - It will be prudent not to try anything too flashy and distracting. _**Definitely** not going to be designed with the same theme as my portfolio page._
 - For clarity of data and stats, ensure good contrast and readabiity
 - However, we should not pessimise the design, we should make sure it is not an eyesore.
 - WIP
 - Should be intuitive to the users. My assumption is that they would be familiar with Microsoft Office.
 I think it will be nice to be able to do a mockup, and to speak to some of the people who would be the _end users_ using the app to see what they would be interested in, and gather some user feedback about things that we are planning to do, to make sure that the user would not hate the software.

## Backend
| Candidates        | General                                                                                                                                                                         | Language                                                                                                                                                                  | Ecosystem                                                     | OpenAPI support |
|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------|-----------------|
| Express (Node.js) | Simple, sufficiently performant, well-used (20.3%, highest framework on SO dev survey)                                                                                          | TypeScript, well-used, easy to write, very good type system. <br><br> This type system can be declared on DefinitelyTyped for better developer experience on the frontend | Slonik for SQL templating and connecting to the sql instances | Through swagger |
| Fastify (Node.js) | More performant than Express, more batteries included, well-used but less commonly known (3.1%) <br><br> Developers' sentiment seems to prefer Fastify because it's more modern | TypeScript                                                                                                                                                                | Same as above                                                 | Yes             |
| FastAPI (Python)  | Simple, also performant, well-used (15.1%)                                                                                                                                      | Python, _most well known language_, especially amongst researchers and clinicians , easy to write.                                                                        | Psycopg + Jinja for templating                                | Yes             |

I have heard about the OpenAPI standard in online forums and someone mentioned to me that I should look it up.

I am going to investigate if it is doable to generate OpenAPI documentation, I think it will be prudent for us to do so. Sticking to the industry standards will prove worthwhile for both people who are trying to access this API, and to find people to maintain it in the future.

## API Documentation
At the beginning, we can use a static site generator that takes markdown files. For ease of documentation during development.

I really enjoy Neon's documentation (https://github.com/neondatabase) for its convenience. Individual API endpoints have sample code which makes it very easy for people to get started and develop. I think it will be interesting to try building something like this _in the future_. For code samples, target curl, JS's fetch API and Python's requests, because these are the most commonly used and the most basic. Because the API documentation is expected to be mostly static, there is no need for us to be using a dynamic site. Definitely no backend for this (except for connecting to the backend for testing)

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