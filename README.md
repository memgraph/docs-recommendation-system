<h1 align="center">
  Docs Recommendation System
</h1>

## :arrow_forward: Starting the app

You can start the app by running:

```
docker-compose build
docker-compose up
```
if you get connection error, please try running `docker-compose up` again.

After loading is done, you can check out the app at `localhost:3000`.

## :mag_right: Look inside Memgraph database

![](/images/app_5.png)

## :art: Graph visualization

Get recommendations based on **node2vec** [MAGE](https://memgraph.com/docs/mage) algorithm and graph visualization of one of the recommended URLs

![](/images/app_1.png)

## :bar_chart: TF-IDF statistics

Check out statistics retrieved with TD-IDF algorithm

![](/images/app_2.png)

## :sparkles: PageRank

Get the **PageRank** [MAGE](https://memgraph.com/docs/mage) algorithm.

![](/images/app_3.png)

## :page_with_curl: Blog post

If you'd like to find out more about the process of building the app, hop on to the [blog post](https://memgraph.com/blog/lost-in-documentation-let-our-docs-recommendation-system-guide-you-along) where we explained it in details!   