/**
 * @author harveyqing
 */
$(document).ready(function(){
    SyntaxHighlighter.autoloader(
        'cpp c                           /static/dopetrope/js/SyntaxHighlighter/shBrushCpp.js',
        'c# c-sharp csharp      /static/dopetrope/js/SyntaxHighlighter/shBrushCSharp.js',
        'css                              /static/dopetrope/js/SyntaxHighlighter/shBrushCss.js',
        'java                             /static/dopetrope/js/SyntaxHighlighter/shBrushJava.js',
        'js jscript javascript     /static/dopetrope/js/SyntaxHighlighter/shBrushJScript.js',
        'text plain                     /static/dopetrope/js/SyntaxHighlighter/shBrushPlain.js',
        'py python                    /static/dopetrope/js/SyntaxHighlighter/shBrushPython.js',
        'sql                               /static/dopetrope/js/SyntaxHighlighter/shBrushSql.js',
        'xml xhtml xslt html      /static/dopetrope/js/SyntaxHighlighter/shBrushXml.js',
        'go                                /static/dopetrope/js/SyntaxHighlighter/shBrushGo.js'
    );
    SyntaxHighlighter.all();
});
