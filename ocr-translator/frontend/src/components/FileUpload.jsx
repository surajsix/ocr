import React, {useState} from 'react'

export default function FileUpload(){
  const [file, setFile] = useState(null)
  const [target, setTarget] = useState('hi')
  const [output, setOutput] = useState('pdf')
  const [loading, setLoading] = useState(false)
  const [downloadUrl, setDownloadUrl] = useState(null)

  const onFile = (e) => {
    setFile(e.target.files[0])
    setDownloadUrl(null)
  }

  const submit = async () => {
    if(!file) return alert('pick a file')
    setLoading(true)
    const fd = new FormData()
    fd.append('file', file)
    fd.append('target', target)
    fd.append('output', output)

    try{
      const res = await fetch('http://localhost:5000/api/translate', {
        method: 'POST',
        body: fd
      })

      if(!res.ok){
        const err = await res.json()
        alert('Server error: ' + (err.error || JSON.stringify(err)))
        setLoading(false)
        return
      }

      // stream the file as blob and create object URL
      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      setDownloadUrl(url)
    }catch(err){
      alert('Request failed: ' + err.message)
    }
    setLoading(false)
  }

  return (
    <div>
      <input type="file" onChange={onFile} accept=".png,.jpg,.jpeg,.pdf" />

      <div style={{marginTop:10}}>
        <label>Target language (ISO code): </label>
        <input value={target} onChange={e=>setTarget(e.target.value)} placeholder="e.g. hi, en, fr" />
      </div>

      <div style={{marginTop:10}}>
        <label>Output:</label>
        <select value={output} onChange={e=>setOutput(e.target.value)}>
          <option value="pdf">PDF</option>
          <option value="text">Text</option>
          <option value="image">Image</option>
        </select>
      </div>

      <div style={{marginTop:12}}>
        <button onClick={submit} disabled={loading}>{loading ? 'Processing...' : 'Translate'}</button>
      </div>

      {downloadUrl && (
        <div style={{marginTop:12}}>
          <a href={downloadUrl} download={`translated.${output === 'text' ? 'txt' : output === 'image' ? 'png' : 'pdf'}`}>
            Download result
          </a>
        </div>
      )}
    </div>
  )
}
