#
# Collective Knowledge (index of CK modules)
#
# 
# 
#
# Developer: 
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

# Local settings

##############################################################################
# Initialize module

def init(i):
    """

    Input:  {}

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    return {'return':0}

##############################################################################
# add index

def add_index(i):
    """
    Input:  {
              dict - index dict
              meta - original CK entry meta
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import copy

    d=i['dict']
    m=i['meta']

    repo_url1_full=d['misc'].get('repo_url1','')

    module_uid=d['misc'].get('module_uid','')

    xworkflow=m.get('workflow','')
    workflow=m.get('workflow_type','')
    if xworkflow=='yes' and workflow=='':
       workflow='yes'

    d['misc']['workflow']=workflow
    d['misc']['actions']={}

    actions=m.get('actions',{})

    if len(actions)>0:
       for q in sorted(actions):

           qq=actions[q]

           d['misc']['actions'][q]={}

           if repo_url1_full!='':
              # Get API!
              l=-1
              rx=ck.get_api({'module_uoa':module_uid, 'func':q})
              if rx['return']==0:
                 l=rx['line']

              if l!=-1:
                 d['misc']['actions'][q]['url_api']=repo_url1_full+'#L'+str(l)

    return {'return':0}

##############################################################################
# generate html

def html(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    d=i.get('dict',{})

    llm=d.get('meta',{})

    llmisc=llm.get('misc',{})
    lldict=llm.get('dict',{})

    desc=lldict.get('desc','')

    duoa=llmisc.get('data_uoa','')
    duid=llmisc.get('data_uid','')

    muoa=llmisc.get('module_uoa','')

    h=''
    if desc!='':
       h+='<i> - '+desc+'</i><br>\n'

    h1=''

    h1+='<a href="http://cknowledge.org/repo/web.php?template=cknowledge&&action=load&out=json&cid=604419a9fcc7a081:befd7892b0d469e9:604419a9fcc7a081" target="_blank">[View meta]</a>&nbsp;\n'


    return {'return':0, 'html':h, 'html1':h1}
