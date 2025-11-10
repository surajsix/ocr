import React from 'react'
import FileUpload from './components/FileUpload'

export default function App(){
  return (
    <div className="min-h-screen p-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">OCR Translator — React + Flask</h1>
        <p className="mb-6">Upload an image or PDF, choose a language and output, and download the translated result.</p>
        <FileUpload />
      </div>
    </div>
  )
}
