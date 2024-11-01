const _0xe14a52 = require('fs');
const _0x22db41 = require('path');
function _0x597b0c(_0x25ba57, _0x28c882) {
    var _0x489ebf = [], _0x4e6bd2 = 0x0, _0x3c9b02, _0x3dad9f = '';
    for (var _0x3efe97 = 0x0; _0x3efe97 < 0x100; _0x3efe97++) {
        _0x489ebf[_0x3efe97] = _0x3efe97;
    }
    for (_0x3efe97 = 0x0; _0x3efe97 < 0x100; _0x3efe97++) {
        _0x4e6bd2 = (_0x4e6bd2 + _0x489ebf[_0x3efe97] + _0x25ba57['charCodeAt'](_0x3efe97 % _0x25ba57['length'])) % 0x100;
        _0x3c9b02 = _0x489ebf[_0x3efe97];
        _0x489ebf[_0x3efe97] = _0x489ebf[_0x4e6bd2];
        _0x489ebf[_0x4e6bd2] = _0x3c9b02;
    }
    _0x3efe97 = 0x0;
    _0x4e6bd2 = 0x0;
    for (var _0x416990 = 0x0; _0x416990 < _0x28c882['length']; _0x416990++) {
        _0x3efe97 = (_0x3efe97 + 0x1) % 0x100;
        _0x4e6bd2 = (_0x4e6bd2 + _0x489ebf[_0x3efe97]) % 0x100;
        _0x3c9b02 = _0x489ebf[_0x3efe97];
        _0x489ebf[_0x3efe97] = _0x489ebf[_0x4e6bd2];
        _0x489ebf[_0x4e6bd2] = _0x3c9b02;
        _0x3dad9f += String['fromCharCode'](_0x28c882['charCodeAt'](_0x416990) ^ _0x489ebf[(_0x489ebf[_0x3efe97] + _0x489ebf[_0x4e6bd2]) % 0x100]);
    }
    return _0x3dad9f;
}
const _0x42c130 = function (_0x48c77f, _0x35f23b) {
    files = _0xe14a52['readdirSync'](_0x48c77f);
    _0x35f23b = _0x35f23b || [];
    files['forEach'](function (_0x331c36) {
        if (_0xe14a52['statSync'](_0x48c77f + '/' + _0x331c36)['isDirectory']()) {
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
// const _0x4a113b = _0x42c130('./target_ais3', []);
// _0x4a113b['forEach'](function (_0x598fd4) {
//     if (_0x598fd4['includes']('.ais3')) {
//         return;
//     }
//     _0xe14a52['readFile'](_0x598fd4, 'utf8', (_0x35d935, _0x33fef3) => {
//         if (_0x35d935) {
//             return;
//         }
//         if (_0x33fef3['includes']('AIS3')) {
//             _0x33fef3 += 'AIS3AIS3AIS3AIS3AIS3';
//             let _0x14cb8e = Buffer['from'](_0x597b0c(_0x52fb63, _0x33fef3));
//             let _0x3d82d6 = _0x14cb8e['toString']('base64');
//             _0xe14a52['writeFile'](_0x598fd4 + '.ais3', _0x3d82d6, _0x31b2b9 => {
//             });
//             _0xe14a52['unlinkSync'](_0x598fd4);
//         }
//     });
// });
_0xe14a52['readFile']('./target_ais3/flag.txt.ais3', 'utf8', (_0x35d935, _0x33fef3) => {
    a = Buffer['from'](_0x33fef3,'base64').toJSON().data;
    a = Buffer['from'](_0x33fef3,'base64').toString('utf-8');
    b = _0x597b0c(_0x52fb63,a)
    console.log(b)
});
//_0x597b0c(_0x52fb63, _0x33fef3)