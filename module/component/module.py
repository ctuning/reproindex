#
# Collective Knowledge (indexing reusable research components)
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
# get index of components

def get(i):
    """
    Input:  {
              (web_vars_post)
              (web_vars_get)
              (web_vars_session)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              html - HTML
            }

    """

    import copy
    import math
    import sys

    wvg=i.get('web_vars_get',{})
    if type(wvg)==list: wvg={}

    wvp=i.get('web_vars_post',{})
    if type(wvp)==list: wvp={}

    wv=copy.deepcopy(wvp)
    wv.update(wvg)

    # Page length
    length=wv.get('l','')
    dlength='10'
    if length=='': length=dlength
    ilength=int(length)

    # Page
    page=wv.get('p','')
    if page=='': page='1'
    ipage=int(page)

    # Check page name
    page_name=i.get('page_name','')
    if page_name=='':
       return {'return':1, 'error':'page_name is empty'}

    # Init URL
    url=page_name+'?'
    url0=url

    # Check component and prepare selector
    c=wv.get('c','')
    if c=='': c='module'

    c_uid='component.*' # Selected UID

    r=ck.access({'action':'load',
                 'module_uoa':'cfg',
                 'data_uoa':'component'})
    if r['return']>0: return r
    di=r['dict'].get('index',[])

    hc=''
    for q in di:
        name=q['name']
        xid=q['id']
        uid=q['uid']

        hc+='<option value="'+xid+'"'
        if xid==c:
           hc+=' selected'
           c_uid=uid
           url+='&c='+xid
        hc+='>'+name+'</option>\n'

    # Check if CID
    cid=wv.get('cid','')
    d_uoa=''
    if cid!='':
       r=ck.parse_cid({'cid':cid})
       if r['return']==0:
          c_uid=r.get('module_uoa','')
          d_uoa=r.get('data_uoa','')

    # Parse search string
    q=wv.get('q','')
    q=q.encode('utf8')

    if '"' in q:
       q1=q.split('"')
    else:
       q1=q.split(' ')
    qs=[]
    for q in q1:
        if q!='':
           if q.startswith(' '):
              q3=q.strip().split(' ')
              q2=[]
              for q in q3:
                  q2.append(q.strip().lower())
           else:
              q2=[q.strip().lower()]
           qs+=q2

    try:    from urllib.parse import urlencode
    except: from urllib import urlencode # pragma: no cover

    qq=urlencode({'q':q})
    if sys.version_info[0]>2: qq=qq.encode('utf8')

    url+='&'+qq

    if ilength!=dlength:
       url+='&l='+str(ilength)

    # Search
    ii={"action":"list",
        "module_uoa":c_uid,
        "add_meta":"yes",
        "filter_func_addr":getattr(sys.modules[__name__],'search_filter'),
        "search_dict":qs}
    if d_uoa!='':
       ii['data_uoa']=d_uoa
    r=ck.access(ii)
    if r['return']>0: return r

    lst=r['lst']
    ep=r['elapsed_time']

    # Sort by name
    lst=sorted(lst, key=lambda x: x.get('meta',{}).get('misc',{}).get('data_uoa',''))

    llst=len(lst)

    x=''
    if llst==0 or llst>1: x='s'
    h=''
    if llst!=1:
       h='<center>'+str(llst)+' result'+x+' ('+("%.3f" % float(ep))+' seconds)<br></center>\n'

    # List
    j1=(ipage-1)*ilength
    j2=((ipage)*ilength)-1
    if j2>=llst: j2=llst-1

    for j in range(j1,j2+1):
        jj=j+1

        ll=lst[j]

        llm=ll['meta']

        llmisc=llm.get('misc',{})

        duoa=llmisc.get('data_uoa','')
        duid=llmisc.get('data_uid','')

        muoa=llmisc.get('module_uoa','')

        r=ck.access({'action':'html',
                     'module_uoa':c_uid,
                     'dict':ll})
        if r['return']>0: return r

        hh=r['html']
        hh1=r.get('html1','')

        xcid=c_uid+':'+duid

        h+='<div id="ck_entries">\n'
        xurl1='<a href="'+url0+'cid='+xcid+'">'
        xurl2='</a>'

        if llst==1:
           h+='<b>'+xurl1+muoa+':'+duoa+xurl2+'</b>\n'
        else:
           h+=str(jj)+') <b>'+xurl1+duoa+xurl2+'</b>\n'

        h+=hh

        if hh1!='':
           h+='<div id="ck_entries_space4"></div>\n'
           h+='<div id="ck_downloads">\n'
           h+=hh1
           h+='</div>\n'

        h+='</div>\n'

        h+='<div id="ck_entries_space4"></div>\n'

    # Get page index
    tpages=int(math.ceil(float(llst)/float(ilength)))

    if tpages>1:
       h+='<p>Pages:&nbsp;&nbsp;&nbsp; '
       h1=''
       for p in range(0, tpages):
           rp=p+1

           url1=url
           if ilength!=dlength:
              url1+='&p='+str(rp)

           x1='<a href="'+url1+'">'
           x2='</a>'
           if rp==ipage:
              x1=''
              x2=''

           if h1!='': h1+=' '
           h1+=x1+str(p+1)+x2

       if (ipage+1)<=tpages:
          url1=url
          url1+='&p='+str(ipage+1)

          h1+='&nbsp;&nbsp;&nbsp; <a href="'+url1+'">Next</a>\n'

       h+=h1

    return {'return':0, 'len':llst, 'html':h, 'html_c':hc}

##############################################################################
# index components

def index(i):
    """
    Input:  {
              (data_uoa)        - which component to index; if "", take from cfg:component
              (target_repo_uoa) - if "", use "reuse-research"
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os
    import copy

    o=i.get('out','')

    tr_uoa=i.get('target_repo_uoa','')
    if tr_uoa=='': tr_uoa='reuse-research'

    # Check which components to index
    duoa=i.get('data_uoa','')
    if duoa!='':
       r=ck.access({'action':'load',
                    'module_uoa':cfg['module_deps']['module'],
                    'data_uoa':duoa})
       if r['return']>0: return r
       duoa=r['data_uid']

    r=ck.access({'action':'load',
                 'module_uoa':cfg['module_deps']['cfg'],
                 'data_uoa':'component'})
    if r['return']>0: return r
    components=r['dict']['index']

    for cc in components:
        name=cc["name"]
        c_uid=cc["uid"]
        cm_uid=cc["orig_module_uid"]

        if duoa!='' and c_uid!=duoa:
           continue

        ck.out('==========================================================')
        ck.out('Indexing component: '+name)
        ck.out('')

        # Search for components
        ii={}
        ii['action']='list'
        ii['module_uoa']=cm_uid
        ii['add_meta']='yes'
        ii['time_out']=-1

        rx=ck.access(ii)
        if rx['return']>0: return rx

        ll=sorted(rx['lst'], key=lambda k: k['data_uoa'])

        repo_url={}
        repo_private={}

        private=''
        num=0

        h=''

        for l in ll:
            ln=l['data_uoa']
            ln_uid=l['data_uid']

            lm_uoa=l['module_uoa']
            lm_uid=l['module_uid']

            lr=l['repo_uoa']
            lr_uid=l['repo_uid']

            url=''
            if lr=='default':
               url='https://github.com/ctuning/ck/tree/master/ck/repo'
            elif lr_uid in repo_url:
               url=repo_url[lr_uid]
            else:
               rx=ck.load_repo_info_from_cache({'repo_uoa':lr_uid})
               if rx['return']>0: return rx
               url=rx.get('dict',{}).get('url','')
               repo_private[lr_uid]=rx.get('dict',{}).get('private','')
               repo_url[lr_uid]=url

            private=repo_private.get(lr_uid,'')

            # Check that repository is not private or local ...
            if lr not in cfg.get('skip_repos',[]) and private!='yes' and url!='':
               num+=1

               ck.out('  '+str(num)+') '+ln)

               # Check if entry already exists
               ddd={}
               exist=False
               r=ck.access({'action':'load',
                            'module_uoa':c_uid,
                            'data_uoa':ln_uid,
                            'repo_uoa':tr_uoa})
               if r['return']>0 and r['return']!=16: return r
               if r['return']==0: 
                  ddd=r['dict']
                  exist=True

               # General vars
               lm=l['meta']
               ld=lm.get('desc','')

               # Info about repo
               if lr=='default':
                  to_get=''
               elif url.find('github.com/ctuning/')>0:
                  to_get='ck pull repo:'+lr
               else:
                  to_get='ck pull repo --url='+url

               repo_url1_full=''
               repo_url2_full=''
               if url!='':
                  url2=url

                  if url2.endswith('.git'):
                     url2=url2[:-4]

                  if '/tree/master/' not in url2:
                     url2+='/tree/master/module/'
                  else:
                     url2+='/module/'

                  repo_url1_full=url2+ln+'/module.py'
                  repo_url2_full=url2+ln+'/.cm/meta.json'

               # Update dict
               ddd['dict']=copy.deepcopy(lm)
               ddd['misc']={'repo_url1':repo_url1_full,
                            'repo_url2':repo_url2_full,
                            'data_uoa':ln,
                            'data_uid':ln_uid,
                            'repo_uoa':lr,
                            'repo_uid':lr_uid,
                            'module_uoa':lm_uoa,
                            'module_uid':lm_uid}

               # Add specific info per component
               r=ck.access({'action':'add_index',
                            'module_uoa':c_uid,
                            'dict':ddd,
                            'meta':lm})
               if r['return']>0: return r

               # Add/update entry
               ii={'module_uoa':c_uid,
                   'data_uoa':ln_uid,
                   'repo_uoa':tr_uoa,
                   'dict':ddd,
                   'substitute':'yes',
                   'sort_keys':'yes'}

               if exist:
                  ii['action']='update'
                  ii['ignore_update']='yes'
               else:
                  ii['action']='add'

               r=ck.access(ii)
               if r['return']>0: return r

        ck.out('')
        ck.out('  Total components: '+str(num))
        ck.out('')

    return {'return':0}

##############################################################################
# search filter

def search_filter(i):

    meta=i.get('meta',{})
    sd=i.get('search_dict',[])

    skip='yes'

    if len(sd)==0:
       skip='no'

    for s in sd:
        for k in meta:
            if not search_filter_recursive(meta[k],s):
               skip='no'
               break

    return {'return':0, 'skip':skip}

##############################################################################
# search filter (recursive)

def search_filter_recursive(v,s):
    skip=True

    if type(v)==list:
       for k in v:
          if not search_filter_recursive(k,s):
             skip=False
             break
    elif type(v)==dict:
        for k in v:
            if not search_filter_recursive(v[k],s):
               skip=False
               break
    else:
        try:
            v=str(v).lower()
        except:
            pass

        if s in v:
           skip=False

    return skip