# pinecone-cli
Pinecode-cli is a command-line interface for control and data plane interfacing with [Pinecone](https://pinecone.io). 

In addition to ALL of the Pinecone "actions/verbs", Pinecone-cli has several additional features that make Pinecone even more powerful including:
   * Upload vectors from CSV files
   * Upload embeddings of text from a given website URL.  Embeddings generated by OpenAI embeddings API.
   * New "head" command to peak into a given index, similar to "head" in linux/unix.

# Install
Feel free to use the tool directly from source here, or just 
```console
pip install pinecone-cli
``` 
Pypi here: (https://pypi.org/project/pinecone-cli/)  Note that the examples below assume you are using the source and have pulled the right deps.  If you install from ```pip``` it gets installed as ```pinecli``` in your PATH.
 
# Usage
First off, let's simplify usage by setting the PINECONE_API_KEY env variable so we don't have to pass it every time in the commandline:
```console
% export PINECONE_API_KEY=1234-4567-abc
```
Otherwise you wind up having to pass the key as so:
```console
% ./pinecli.py query --apikey=1234 ....
```


The pattern for using the tool is to invoke 'pinecli' and then use a command.  The list of commands appears with --help

```console
% ./pinecli.py --help
Usage: pinecli.py [OPTIONS] COMMAND [ARGS]...

  A command line interface for working with Pinecone.

Options:
  --help  Show this message and exit.

Commands:
  configure-index-pod-type  Configures the given index to have a pod type.
  configure-index-replicas  Configures the number of replicas for a given
                            index.
  create-collection         Creates a Pinecone collection from the argument
                            'source_index'
  create-index              Creates a Pinecone Index.
  delete-collection         Deletes a collection.
  delete-index              Deletes an index.  You will be prompted to
                            confirm.
  describe-collection       Describes a collection.
  describe-index            Describes an index.
  describe-index-stats      Prints out index stats to stdout.
  fetch                     Fetches vectors from Pinecone specified by the
                            vectors' ids.
  head                      Shows a preview of vectors in the
                            <PINECONE_INDEX_NAME>
  list-collections          Lists collections for the given apikey.
  list-indexes              Lists the indexes for your api key.
  query                     Queries Pinecone with a given vector.
  update                    Updates the index based on the given id passed in.
  upsert                    Extracts text from url arg, vectorizes w/ openai
                            embedding api, and upserts to Pinecone.
  upsert-file               Upserts a file (csv) into the specified index.
  upsert-random             Upserts a vector(s) with random dimensions into
                            the specified vector.
  upsert-webpage            Extracts text from url arg, vectorizes w/ openai
                            embedding api, and upserts to Pinecone.
```

# Commands With Examples
Before you can use Pinecone an index is required.  We can now do this on the commandline rather than in the UI: (Note not all of the cmdline options are required, they're shown here to demonstrate functionality and control)
```console
% ./pinecli.py create-index myindex --dims=1536 --metric=cosine --pods=2 --replicas=2 --shards=1 --pod-"type=p2.x1"
```

Note that for any command, if you want an exhasuive description of cmdline options, simply do something similar to the below, where "create-index" is replaced by one of the commands:
```console
% ./pinecli.py create-index --help
Usage: pinecli.py create-index [OPTIONS] PINECONE_INDEX_NAME

  Creates the Pinecone index named <PINECONE_INDEX_NAME>

Options:
  --apikey TEXT             Pinecone API Key
  --region TEXT             Pinecone Index Region
  --dims INTEGER            Number of dimensions for this index  [required]
  --metric TEXT             Distance metric to use.  [required]
  --pods INTEGER            Number of pods  [default: 1]
  --replicas INTEGER        Number of replicas  [default: 1]
  --shards INTEGER          Number of shards  [default: 1]
  --pod-type TEXT           Type of pods to create.  [required]
  --source_collection TEXT  Source collection to create index from
  --help                    Show this message and exit.
  ```

Let's try some commands showing two missing features I'd love to have had over the last year: a "head" command and a quick "stats" command:

## Index Stats Including Number of Vectors
``` console
% ./pinecli.py describe-index-stats myindex
Dimensions: 1536
Vectors: 7745
Index_Fullness: 0.0
Namespace data:
        : 7745
```

## Head command to preview vectors
``` console
% ./pinecli.py head kids-facenet
{'matches': [{'id': 'bubba_50.jpg.vec',
              'metadata': {},
              'score': 12.182938,
              'values': [-0.016061664,
                         -0.4495437,
                         -0.034082577,
                         .....
```

Now, let's query some nonsensical data from the index named 'upsertfile'

## Inserting a vector directly 
*Note the double quites around the vector*
```console
% ./pinecli.py query myindex  "[1.2, 1.0, 3.0]" --print-table  --include-meta=True
                      🌲 upsertfile ns=() Index Results                      
┏━━━━━━┳━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃   ID ┃ NS ┃ Values                   ┃                Meta ┃        Score ┃
┡━━━━━━╇━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ vec1 │    │ 0.1,0.2,0.3              │  {'genre': 'drama'} │    0.9640127 │
│ vec2 │    │ 0.2,0.3,0.4              │ {'genre': 'action'} │    0.9552943 │
│  abc │    │ 0.23223,-1.333,0.2222222 │      {'foo': 'bar'} │ -0.083585836 │
│  ghi │    │ 0.23223,-1.333,0.2222222 │      {'bar': 'baz'} │ -0.083585836 │
└──────┴────┴──────────────────────────┴─────────────────────┴──────────────┘
```

Markdown of course does a great job of mangling great terminal output so here's a screenshot from using ```---print-table```:
![alt](https://github.com/tullytim/pinecone-cli/blob/main/head-print.png?raw=true)


You can of course not output the pretty table by removing ```--print-table```:
```console
% ./pinecli.py query myindex "[1.2, 1.0, 3.0]" --include-meta=True
{'matches': [{'id': 'vec1',
              'metadata': {'genre': 'drama'},
              'score': 0.9640127,
              'values': [0.1, 0.2, 0.3]},
              ...
```

## Upsert Vectors in Command Line Manually
Following the Pinecone vector format of the tuple formatted as:
```python
('vectorid', [vecdim1, vecdim2, vecdim3], {'metakey':'metaval'})
```
You can pass this in as a comma separated list of vectors on the command line:
```console
./pinecli.py upsert myindex "[('vec1', [0.1, 0.2, 0.3], {'genre': 'drama'}), ('vec2', [0.2, 0.3, 0.4], {'foo': 'bar'}),]"
```

## Upsert CSV file
Upserting a csv file is trivial.  Simply create your csv file with any headings you have, but there must be at least a labeled id column and a labeled vector column for the vectors.  Here's an example of a CSV file that is clearly a DataFrame dump due to the index column on the left which works great w/ pinecone-cli:
```console
index,my_id_column,my_vectors_column,Metadata
1,abc,"[0.23223, -1.333, 0.2222222]",{'foo':'bar'}
2,ghi,"[0.23223, -1.333, 0.2222222]",{'bar':'baz'}
```
The name of those columns in the header row can be arbitrary or you can name then "id", "vectors" and "metadata" which is our default assumption.  If you have custom column names and don't want to change them, just pass in the ```--colmap``` argument which takes in a python dictionary mapping "id" and "vectors" to the naming you have in your csv.  For example:
```"{"id":"my_id_column", "vectors":"my_vectors_column"}```

Note that as in other CSV file for Dataframes, we need an index column as in the example above.
Here's an example using the CSV headers and format above with the correct colmap argument:
```console
% ./pinecli.py upsert-file  embeddings.csv myindex "{'id':'my_id_column', 'vectors':'my_vectors_column'}"
```

### More on CSV Formatting
For now you will need to manually provide an index column (we are using dataframes under the hood.)


## Upserting Vector Embeddings of Webpage Text!
pinecone-cli was built to make using Pinecone extremely easy and fast.  We have integrated [OpenAI](https://openai.com/) (others coming) - using its [embedding APIs](https://platform.openai.com/docs/guides/embeddings) to fetch embeddings.  We then upload them into your index for you, making uploading embeddings of an entire website's text - trivial.
```console
% ./pinecli.py upsert-webpage https://menlovc.com lpfactset  --openaiapikey=12345-9876-abcdef
[nltk_data] Downloading package punkt to /Users/tim/nltk_data...
[nltk_data]   Package punkt is already up-to-date!
100%|████████████████████████████████████████████████████████████████████████| 5/5 [00:00<00:00, 61680.94it/s]
['About Us  Our Promise  Focus Areas   Consumer  Cloud Infrastructure  Cybersecurity  Fintech  Healthcare  SaaS  Supply Chain and Automation    Team  Portfolio  Perspective            When we invest, we’re invested. Our promise to founders        Building a business is a team sport. As investors, we don’t just sit on the sidelines but do whatever it takes to help our teams win. About Us    The founders we back don’t limit themselves to what is, but relentlessly pursue what could be. We invest in transformative technology companies that are changing the way we live and work. Portfolio    Menlo Labs starts companies. We work shoulder-to-shoulder 
....
100%|█████████████████████████| 1/1 [00:00<00:00,  1.11it/s]
```

## Upsert Random Vectors
One of the more useful things we can do with pinecone-cli is insert random vectors, primarily for testing.  Often we will create our index and the length of the vector will be 1,536 dimensions, for example.  Instead of writing a bunch of code to go suddenly create those vectors somehow, we can use pinecone-cli to start generating vectors and upserting them:
```console
% ./pinecli.py upsert-random  upsertfile  --num_vector_dims=1536 --num_vectors=10 --debug                                                                                                                                      
upserted_count: 10
1it [00:00,  4.36it/s]  
```
The example above inserts 10 vectors that each have 1,536 random vectors in them. Note that the ```id``` for each vector is simply ```f'id-{i}'``` where is is the ith row (vector) inserted.

## Query Vectors
Querying can be done in two ways on the cmdline - pass in an actual vector string literal, or ask Pinecone to query randomly (maybe you want to just look at them or look at a TSNE).  In the example below, the last argument (required) is either the string 'random' or an actual vector such as '[0.0, 1.0, 3.14569]'.  Let's try random:
```console
% ./pinecli.py query myindex random
```

You can also plot a TSNE plot to view clustering of your vectors by using the ```-show-tsne=True``` flag.  Note that this will pop up the plt plot by default. 

```console
% ./pinecli.py query lpfactset random --show-tsne=true --topk=2500 --num-clusters=4
```

![alt](https://github.com/tullytim/pinecone-cli/blob/main/tsne.png?raw=true)

## Fetching Vectors:
Fetching is simple - just pass in the vector id(s) of the vectors you're looking for as a comma separated list:
```console
% ./pinecli.py fetch myindex --vector_ids="05b4509ee655aacb10bfbb6ba212c65c,c626975ec096b9108f158a56a59b2fd6"

{'namespace': '',
 'vectors': {'05b4509ee655aacb10bfbb6ba212c65c': {'id': '05b4509ee655aacb10bfbb6ba212c65c',
                                                  'metadata': {'content': 'Chime '
                                                                          'Scholar '
                                                                          'spotlight: '
```

## Updating Vectors
Updating vectors is simple - pass the id of the vector and the updating vector as below:
```console
% ./pinecli.py update "id-9" myindex  "[0.0, 1.0, 3.0]"
```
## List Operations
pinecone-cli has all of the necessary 'list' operations as shown below:

### List Indexes
This gives you a list of all indexes under your api key:
```console
% ./pinecli.py list-indexes                                    
cli
cli2
cli3
drivertest
```
### List Collections
This obviously lists the collections you've created:
```console
% ./pinecli.py list-collections                                    
cli
cli2
cli3
drivertest
```

### Other Meta Operations
We showed the "describe-index-stats" command at the top of this page.  There is also "describe-index" which provides the following:
```console
% ./pinecli.py describe-index lpfactset
Name: lpfactset
Dimensions: 1536
Metric: cosine
Pods: 1
PodType: p2.x1
Shards: 1
Replicas: 1
Ready: True
State: Ready
Metaconfig: None
Sourcecollection: 
```

### Describe Collections
```console
% ./pinecli.py describe-collection testcoll
Name: testcoll
Dimensions: 1536
Vectors: 124
Status: Ready
Size: 3917544
```

## Deleting Indexes
Deleting an index is straightforward.  To prevent catastrophic accidents, you'll be prompted to type in the name of the index backwards:
```console
 ./pinecli.py delete-index myindex2
Type name of index backwards to confirm: : 2xedniym
```
