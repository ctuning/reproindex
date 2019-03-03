#
# Collective Knowledge (index of CK repositories)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin
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
    import os

    d=i['dict']
    m=i['meta']

    dd=d.get('dict',{})

    if 'misc' not in d: d['misc']={}
    misc=d['misc']

    repo_url1_full=misc.get('repo_url1','')
    repo_url2_full=misc.get('repo_url2','')
    repo_url3_full=misc.get('repo_url3','')

    data_uoa=misc.get('data_uoa','')
    data_uid=misc.get('data_uid','')

    module_uoa=misc.get('module_uoa','')
    module_uid=misc.get('module_uid','')

    # Find real repo and get .ckr.json
    ckr={}
    rx=ck.access({'action':'where',
                  'module_uoa':cfg['module_deps']['repo'],
                  'data_uoa':data_uoa})
    if rx['return']==0: 
       pckr=os.path.join(rx['path'], ck.cfg['repo_file'])
       if os.path.isfile(pckr):
          rx=ck.load_json_file({'json_file':pckr})
          if rx['return']>0: return rx

          rxd=rx['dict']

          dx=rxd['dict']

          if 'path' in dx:
             del(dx['path'])

          real_repo_uid=rxd['data_uid']

          # Check if mismatch of real uid and current one (old bug - should be fixed now)
          if real_repo_uid!=data_uid:
             ck.out('')
             ck.out('WARNING: repo UID mismatch for '+data_uoa+' ('+real_repo_uid+' != '+data_uid+')')
             ck.out('')
          else:
             ckr=dx

    misc['ckr']=ckr

    # Check extra info
    r=ck.access({'action':'load',
                 'module_uoa':cfg['module_deps']['cfg'],
                 'data_uoa':cfg['cfg-list-of-repos']})
    if r['return']==0:
       dx=r['dict']

       d1=dx.get(data_uid,{})
       if len(d1)>0:
          d=d1.get('dict',{})

          url=d.get('url','')
          external_url=d.get('external_url','')
          rd=d.get('repo_deps',{})

          ld=d.get('desc','')
          ld=ld.replace('$#repo_url#$',repo_url3_full)

          misc['desc']=ld

          workflow_desc=d.get('workflow_desc','')
          
          workflow_desc=workflow_desc.replace('$#repo_url#$',repo_url3_full)

          if d.get('ck_artifact','')!='' or d.get('reproducible_article','')=='yes' or d.get('passed_artifact_evaluation','')=='yes':
             if workflow_desc!='': workflow_desc+='<p>'
             workflow_desc+='reproducible&nbsp;paper\n'
             if d.get('passed_artifact_evaluation','')=='yes':
                workflow_desc+='-&nbsp;passed&nbsp;<a href="http://cTuning.org/ae">Artifact&nbsp;Evaluation</a>:\n'
                workflow_desc+='<p><center><img src="https://www.acm.org/binaries/content/gallery/acm/publications/replication-badges/artifacts_evaluated_reusable_dl.jpg" width="64"></center>\n'

          misc['workflow_desc']=workflow_desc

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

    workflow=llmisc.get('workflow','')

    repo_url1=llmisc.get('repo_url1','')
    repo_url2=llmisc.get('repo_url2','')

    desc=lldict.get('desc','')

    duoa=llmisc.get('data_uoa','')
    duid=llmisc.get('data_uid','')

    ruoa=llmisc.get('repo_uoa','')
    ruid=llmisc.get('repo_uid','')

    muoa=llmisc.get('module_uoa','')

    h=''
    if desc!='':
       h+='<i> - '+desc+'</i>\n'

    actions1=lldict.get('actions',{})
    actions2=llmisc.get('actions',{})

    h+='<div style="background-color:#efefef;margin:5px;padding:5px;">\n'
    if len(actions1)>0:
       h+='<b>Repo name:</b> '+ruoa+'<br>\n'
       if workflow!='':
          h+='<b>Workflow:</b> '+workflow+'<br>\n'
       h+='<b>Actions:</b><br>\n'
       h+='<div style="margin-left:20px;">\n'
       h+=' <ul>\n'
       for a in actions1:
           x=actions1[a]
           ad=x.get('desc','')
           y=actions2.get(a,{})
           au=y.get('url_api','')

           h+='  <li><span style="color:#2f0000;">ck <i>'+str(a)+'</i> '+duoa+'</span> - '+ad
           if au!='':
              h+=' [<a href="'+au+'"><b><span style="color:#2f0000;">API</span></b></a>]\n'

       h+=' </ul>\n'
       h+='</div>\n'
    h+='</div>\n'

    h1=''

    if repo_url1!='':
       h1+='[&nbsp;<a href="'+repo_url1+'" target="_blank">code</a>&nbsp;] \n'
    if repo_url2!='':
       h1+='[&nbsp;<a href="'+repo_url2+'" target="_blank">meta</a>&nbsp;]\n'

    return {'return':0, 'html':h, 'html1':h1}
