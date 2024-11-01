const fs = require('fs');
const _0x22db41 = require('path');
function enc_f(enc, data) {
    var num = [], idx = 0x0, tmp, _0x3dad9f = '';
    for (var i = 0x0; i < 0x100; i++) {
        num[i] = i;
    }
    for (i = 0x0; i < 0x100; i++) {
        idx = (idx + num[i] + enc['charCodeAt'](i % enc['length'])) % 0x100;
        tmp = num[i];
        num[i] = num[idx];
        num[idx] = tmp;
    }
    console.log(num)
    i = 0x0;
    idx = 0x0;
    b = [];
    for (var j = 0x0; j < data['length']; j++) {
        i = (i + 0x1) % 0x100;
        idx = (idx + num[i]) % 0x100;
        tmp = num[i];
        num[i] = num[idx];
        num[idx] = tmp;
        a = num[(num[i] + num[idx]) % 0x100];

        b[j] = a;
        _0x3dad9f += String['fromCharCode'](data['charCodeAt'](j) ^ a);

    }
    console.log(b);
    return _0x3dad9f;
}
const _0x42c130 = function (_0x48c77f, _0x35f23b) {
    files = fs['readdirSync'](_0x48c77f);
    _0x35f23b = _0x35f23b || [];
    files['forEach'](function (_0x331c36) {
        if (fs['statSync'](_0x48c77f + '/' + _0x331c36)['isDirectory']()) {
            _0x35f23b = _0x42c130(_0x48c77f + '/' + _0x331c36, _0x35f23b);
        } else {
            _0x35f23b['push'](_0x22db41['join'](__dirname, _0x48c77f, '/', _0x331c36));
        }
    });
    return _0x35f23b;
};
var _0x59ef93 = process['argv']['slice'](0x2);
if (_0x59ef93['length'] > 0x0) {
    var _0x52fb63 = _0x59ef93[0x0];
}

// data = fs.readFileSync('./target_ais3/flag.txt.ais3', 'utf8');
// let buff = Buffer.from(data, 'base64');
// let text = buff.toString('ascii');
// console.log(text)

a = '\xc2\xb4\xc2\x8e\x07j\xc2\xbc@\x14\xc2\x8eY\x00\xc3\x88\xc2\x91\xc2\xbc\xc2\xabR\x04\x1a\xc3\x9a\xc3\x95}\xc2\x88\xc3\x92\xc3\x80\xc3\xa1\xc3\x90h\xc2\xabb\xc2\x9c\xc3\xb2\xc2\xa6\xc3\x81\x1b=\xc2\xa3\xc2\xb4\xc3\xbd>\xc3\xa0\xc3\x8fe\xc2\x91\xc3\x87\xc3\x82\xc2\xa2\xc2\xae\xc2\x81eV\xc2\xb7o\xc3\xaf:\xc3\xaf\x15\x05Vx\xc2\xa8\xc2\x8c\xc3\xb7\xc2\x9f\xc3\xa6\xc2\x8eX\xc3\x95\xc3\x84x\xc2\xa0\xc2\xb2'
a = "\xc2\xb4\xc2\x8e\x07j\xc2\x86h\x18\xc3\x8fy'\xc3\xa8\xc3\x8d\xc2\x90\xc2\x95`E>\xc3\x8c\xc3\xb2/\xc2\xbb\xc3\xbc\xc3\xb6\xc2\xa6"
f = enc_f(_0x52fb63,a)
console.log(f)
// const _0x4a113b = _0x42c130('./target_ais3', []);
// _0x4a113b['forEach'](function (_0x598fd4) {
//     if (_0x598fd4['includes']('.ais3')) {
//         return;
//     }
//     fs['readFile'](_0x598fd4, 'utf8', (_0x35d935, _0x33fef3) => {
//         if (_0x35d935) {
//             return;
//         }
//         if (_0x33fef3['includes']('AIS3')) {
//             _0x33fef3 += 'AIS3AIS3AIS3AIS3AIS3';
//             let _0x14cb8e = Buffer['from'](enc(_0x52fb63, _0x33fef3));
//             let _0x3d82d6 = _0x14cb8e['toString']('base64');
//             fs['writeFile'](_0x598fd4 + '.ais3', _0x3d82d6, _0x31b2b9 => {
//             });
//             fs['unlinkSync'](_0x598fd4);
//         }
//     });
// });