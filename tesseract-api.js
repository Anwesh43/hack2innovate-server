const childProcess = require('child_process')
const fs = require('fs')
class TesseractApi {
    getTextFromImage(fileName) {
        return new Promise((resolve,reject)=>{
          childProcess.execSync(`tesseract ${fileName} ${fileName_txt}`)
          try {
              var stream = fs.createReadStream(`${fileName_txt}.txt`)
              var msg = ''
              stream.on('data',(data)=>{
                  msg = `${msg}${data.toString()}`
              })
              stream.on('end',()=>{
                  resolve(msg)
              })
          }
          catch(e) {
              reject(e)
          }
      })
    }
}
const tesseractApi = new TesseractApi()
module.exports = tesseractApi
