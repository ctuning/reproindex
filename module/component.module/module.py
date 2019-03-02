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

    repo_url1=llmisc.get('repo_url1','')
    repo_url2=llmisc.get('repo_url2','')

    desc=lldict.get('desc','')

    duoa=llmisc.get('data_uoa','')
    duid=llmisc.get('data_uid','')

    muoa=llmisc.get('module_uoa','')

    h=''
    if desc!='':
       h+='<i> - '+desc+'</i>\n'

    actions1=lldict.get('actions',{})
    actions2=llmisc.get('actions',{})

    h+='<div style="background-color:#efefef;margin:5px;padding:5px;">\n'
    if len(actions1)>0:
       h+='<b>Actions:</b><br>\n'
       h+='<div style="margin-left:20px;">\n'
       h+=' <ul>\n'
       for a in actions1:
           x=actions1[a]
           ad=x.get('desc','')
           y=actions2.get(a,{})
           au=y.get('url_api','')

           h+='  <li><span style="color:#9f0000;">ck <i>'+str(a)+'</i> '+duoa+'</span> - '+ad
           if au!='':
              h+=' (&nbsp;<a href="'+au+'">API</a>&nbsp;)\n'

       h+=' </ul>\n'
       h+='</div>\n'
    h+='</div>\n'

    h1=''

    if repo_url1!='':
       h1+='[&nbsp;<a href="'+repo_url1+'" target="_blank">code</a>&nbsp;]&nbsp;\n'
    if repo_url2!='':
       h1+='[&nbsp;<a href="'+repo_url2+'" target="_blank">meta</a>&nbsp;]\n'


    return {'return':0, 'html':h, 'html1':h1}
