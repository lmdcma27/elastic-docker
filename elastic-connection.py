from elasticsearch import Elasticsearch

import warnings
warnings.filterwarnings("ignore")  

def Connection(es_host,es_user,es_password,api_key):
        es = Elasticsearch( hosts=[es_host], basic_auth=(es_user, es_password), verify_certs=False,api_key=api_key)
        return es

def create_repository(conn, repository_name='my_fs_backup'):
        # Snapshot repository settings
        repository_type = 'fs'
        repository_settings = {            
            "location": "/usr/share/elasticsearch/backups",
            "compress": "true"
        }
        response = conn.snapshot.create_repository(repository_name, body={
            "type": repository_type,
            "settings": repository_settings
        }, request_timeout=30)

        print(response)
        
        
def create_snapshot(conn,index_name):

        # Snapshot repository name
        repository_name = 'my_fs_backup'
        snapshot_name = index_name+'_snapshot-' # Replace with a suitable name for your snapshot
        try:
            response = conn.snapshot.create(repository=repository_name, snapshot=snapshot_name, body={
                "indices": index_name,
                "include_global_state": False
            }, request_timeout=300)

            print(response)
        except:
            print('No existe tal índice')
                    
        
def create_index(conn,name):
    if name in conn.indices.get('*').keys():
        print("This index already exists")
    else:
        print("New index created")
        conn.indices.create(index=name) 


def list_repositories(conn):
        # List snapshot repositories
        repositories = conn.snapshot.get_repository()
        print("Snapshot Repositories:")
        for repo_name in repositories:
            print(repo_name)      
            
def list_snapshots(conn):
    # List snapshots
    repository_name = 'my_fs_backup'        
    snapshots = conn.snapshot.get(repository=repository_name, snapshot='_all')
    print("Snapshots:")
    for snapshot in snapshots['snapshots']:
        print(snapshot['snapshot'])
        
def list_indices(conn):
    indices = conn.indices.get('*')
    print("Indices:")
    print(indices.keys())    

def restore_snapshot(conn,snapshot_name,index_name):

    # Snapshot repository name
    repository_name = 'my_fs_backup'
        
    # Restore the snapshot
    response = conn.snapshot.restore(repository=repository_name, snapshot=snapshot_name, body={
        "indices": index_name
    }, request_timeout=300)
    print(response)


api_key=('CipixYsBfwFa9qIttikK','2DgJCZ7RTOGdTAMixwYO5Q')

es=Connection('https://localhost:9200/','elastic','brA+oDAgA1wAnIXMtk_N',api_key)


#es.index(index='favorite_mangas',body={'Manga':'One Piece','Author':'Eiichiro Oda','Year':'1997'})
#es.index(index='favorite_mangas',body={'Manga':'Hunter x Hunter','Author':'Yoshihiro Togashi ','Year':'1999'})
#es.index(index='favorite_mangas',body={'Manga':'Naruto','Author':'Masashi Kishimoto','Year':'1998'})
#print(es.search(index='favorite_mangas',body={'query':{'match_all':{}}} ))