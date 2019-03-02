#
# Collective Knowledge (indexing reusable research components)
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

    # Check search
    q=wv.get('q','')

    try:    from urllib.parse import urlencode
    except: from urllib import urlencode # pragma: no cover

    qq=urlencode({'q':q})
    if sys.version_info[0]>2: qq=qq.encode('utf8')

    url+='&'+qq

    if ilength!=dlength:
       url+='&l='+str(ilength)

    # Search
    ii={"action":"search",
        "module_uoa":c_uid,
        "add_meta":"yes"}
    r=ck.access(ii)
    if r['return']>0: return r

    lst=r['lst']
    ep=r['elapsed_time']

    llst=len(lst)

    x=''
    if llst==0 or llst>1: x='s'
    h='<center>'+str(llst)+' result'+x+' ('+("%.3f" % float(ep))+' seconds)<br></center>\n'

    # List
    j1=(ipage-1)*ilength
    j2=((ipage)*ilength)-1
    if j2>=llst: j2=llst-1

    for j in range(j1,j2+1):
        jj=j+1
        h+=str(jj)+'<br>\n'



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
