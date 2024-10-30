(async ()=>{
  const urls = process.argv[2].split(',')
  var cache = {}

  for(let url of urls){
    url = url.trim()
    let parsed_url= url.match(/https?:\/\/(?<host>[^\/]*)\/(?<path>.*)/)
    let { host, path } = parsed_url?.groups || {}
    if(!parsed_url || !host || host?.match(/localhost/i)){
      console.log(`<pre>Invalid URL: ${url}\n(doesn't match /https?:\\/\\/(?<host>[^\\/]*)\\/(?<path>.*)/)</pre>`)
      continue
    }

    cache[host] = cache[host] || {}
    await fetch(url).then(r=>r.text()).then(text=>{
      let result
      try{
        result = JSON.parse(text)
      }catch{
        result = text
      }
      cache[host][path] = result
    }).catch(()=>{})
  }
  for(let host of Object.keys(cache)){
    for(let path of Object.keys(cache[host])){
      console.log(`<h3>${host}/${path}<h3>`)
      console.log(`<pre>${JSON.stringify(cache[host][path],null,4)}</pre>`.replaceAll('\\n',''))
    }
  }
  
})()

