function breizHash(string, method)  {   
    if (!('ENCRYPT' == method || 'DECRYPT' == method)) {
        method = 'ENCRYPT';
    }
    if ('ENCRYPT' == method){
        var output = '';
        for (var x = 0, y = string.length, charCode, hexCode; x < y; ++x) {
            charCode = string.charCodeAt(x);
            if (128 > charCode) {
                charCode += 128;       
            } else if (127 < charCode) {
                charCode -= 128;
            }       
            charCode = 255 - charCode;
            hexCode = charCode.toString(16);
            if (2 > hexCode.length) {         
                hexCode = '0' + hexCode;       
            }        
            output += hexCode;     
        }     
        return output;   
