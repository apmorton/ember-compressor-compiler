exports = new Object();

function precompile(source) {
    var compiled = exports.precompile(source);
    return compiled.toString();
}