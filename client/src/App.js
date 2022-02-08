import React, { useEffect, useState } from 'react'
import axios from 'axios'

function App() {

  const [index, setIndex] = useState([])
  const [document, setDocument] = useState([])

  useEffect(() => {
    const getData = async () => {
      const { data } = await axios.get('/api/documents/')
      const newIndex = []
      for (let i = 0; i < data.length; i++) {
        newIndex.push(data[i].id)
      }
      setIndex(newIndex)
    }

    getData()
  }, [])

  useEffect(() => {
    const getWords = async () => {
      const newData = []
      for (let i = 0; i < index.length; i++) {
        const  info  = await axios.get(`/api/documents/${index[i]}/`)
        newData.push(info.data)
      }
      setDocument(newData)
    }
    getWords()
  }, [index])
  


  
  return (
    <>
      <h1>
        {document.map(doc => {
          return (
            <section key={doc[0]} style={{  padding: '100px' }} >
              <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '30px' }}>Document - {doc[0]}</div>
              <div style={{ display: 'flex', justifyContent: 'center', fontSize: '18px', padding: '0 200px 0 200px', fontWeight: 'bolder' }}>
                <div style={{ width: '30%', border: 'solid 1px', padding: '20px' }}>Words</div>
                <div style={{ width: '20%', border: 'solid 1px', padding: '20px' }}>Occurences</div>
                <div style={{ width: '50%', border: 'solid 1px', padding: '20px' }}>Sentences</div>
              </div>
              {doc.map(info => {
                if (typeof info !== 'string') {
                  return (
                    <div key={info[0]} style={{ display: 'flex', justifyContent: 'center', fontSize: '15px', padding: '0 200px 0 200px' }}>
                      <div style={{ width: '30%', border: 'solid 1px', padding: '20px' }}>{info[0]}</div>
                      <div style={{ width: '20%', border: 'solid 1px', padding: '20px'  }}>{info[1]} </div>
                      <div style={{ width: '50%', border: 'solid 1px', padding: '20px'  }}>
                        {info[2].map(sentence => {
                          return (
                            <p key={sentence.length}>...{sentence}...</p>
                          )
                        })}
                      </div>
                    </div>
                  )
                }
              })}
            </section>
          )
        })}
      </h1>
    </>
  )
}

export default App
