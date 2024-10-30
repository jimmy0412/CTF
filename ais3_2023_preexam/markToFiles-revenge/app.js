const express = require('express')
const path = require('path')
const {Pandoc, OutputFormat} = require('@hackmd/pandoc.js')
const crypto = require('crypto')
const fs = require('fs')
const app = express()
const port = 3001
const outputFormats = {
  asciidoc: 'text/plain',
  markdown: 'text/plain',
  latex: 'application/x-latex',
}
const cache = {}
for (const f in OutputFormat) {
  cache[f] = {}
}
async function actionPandoc(req, res) {
  const pandoc = new Pandoc()

  const from = '/tmp/' + Date.now() + '.md'
  const content = req.body.comment
  const exportType = req.body.options
  const title = req.body.title
  const hash = content.substring(0, 10)
  if (!(exportType in OutputFormat)) {
    return res.json({message: 'format not found'})
  }

  if (/\.\./.test(title) || /[^a-zA-Z0-9._();'"-]/.test(title)) {
    return res.json({
      message: 'h@ck3r found!',
    })
  }

  if (cache[exportType][hash] === undefined) {
    cache[exportType][hash] = req.body.title
    const to = '/tmp/' + req.body.title

    fs.writeFileSync(from, content)
    try {
      await pandoc.convertFromFile(from, exportType, to, ['--metadata', `title=${title}`])
    } catch (err) {
      fs.writeFileSync(to, err.message)
    }
  }
  var filename = cache[exportType][hash]
  var stream = fs.createReadStream('/tmp/' + filename)
  filename = encodeURIComponent(filename)

  res.setHeader('Content-disposition', `attachment; filename="${filename}.${exportType}"`)
  res.setHeader('Cache-Control', 'private')
  res.setHeader('Content-Type', `${outputFormats[exportType]}; charset=UTF-8`)
  res.setHeader('X-Robots-Tag', 'noindex, nofollow')

  stream.pipe(res)
}

app.use(express.urlencoded())

app.use(express.json())

app.get('/', function (req, res) {
  res.sendFile(path.join(__dirname + '/public', '/index.html'))
})
app.post('/api/generate', function (req, res) {
  try {
    actionPandoc(req, res)
  } catch (e) {
    res.send('Internal Error')
  }
})

app.listen(port)
console.log('Server started at http://localhost:' + port)
