// http://code.google.com/p/jquery-jsonp/
(function(a){function b(){}function c(a){B=[a]}function d(a,b,c,d){try{d=a&&a.apply(b.context||b,c)}catch(e){d=!1}return d}function e(a){return/\?/.test(a)?"&":"?"}function E(l){function Y(a){R++||(S(),L&&(z[N]={s:[a]}),H&&(a=H.apply(l,[a])),d(E,l,[a,t]),d(G,l,[l,t]))}function Z(a){R++||(S(),L&&a!=u&&(z[N]=a),d(F,l,[l,a]),d(G,l,[l,a]))}l=a.extend({},C,l);var E=l.success,F=l.error,G=l.complete,H=l.dataFilter,I=l.callbackParameter,J=l.callback,K=l.cache,L=l.pageCache,M=l.charset,N=l.url,O=l.data,P=l.timeout,Q,R=0,S=b,T,U,V,W,X;return w&&w(function(a){a.done(E).fail(F),E=a.resolve,F=a.reject}).promise(l),l.abort=function(){!(R++)&&S()},d(l.beforeSend,l,[l])===!1||R?l:(N=N||h,O=O?typeof O=="string"?O:a.param(O,l.traditional):h,N+=O?e(N)+O:h,I&&(N+=e(N)+encodeURIComponent(I)+"=?"),!K&&!L&&(N+=e(N)+"_"+(new Date).getTime()+"="),N=N.replace(/=\?(&|$)/,"="+J+"$1"),L&&(Q=z[N])?Q.s?Y(Q.s[0]):Z(Q):(v[J]=c,V=a(s)[0],V.id=k+A++,M&&(V[g]=M),D&&D.version()<11.6?(W=a(s)[0]).text="document.getElementById('"+V.id+"')."+n+"()":V[f]=f,p in V&&(V.htmlFor=V.id,V.event=m),V[o]=V[n]=V[p]=function(a){if(!V[q]||!/i/.test(V[q])){try{V[m]&&V[m]()}catch(b){}a=B,B=0,a?Y(a[0]):Z(i)}},V.src=N,S=function(a){X&&clearTimeout(X),V[p]=V[o]=V[n]=null,x[r](V),W&&x[r](W)},x[j](V,y),W&&x[j](W,y),X=P>0&&setTimeout(function(){Z(u)},P)),l)}var f="async",g="charset",h="",i="error",j="insertBefore",k="_jqjsp",l="on",m=l+"click",n=l+i,o=l+"load",p=l+"readystatechange",q="readyState",r="removeChild",s="<script>",t="success",u="timeout",v=window,w=a.Deferred,x=a("head")[0]||document.documentElement,y=x.firstChild,z={},A=0,B,C={callback:k,url:location.href},D=v.opera;E.setup=function(b){a.extend(C,b)},a.jsonp=E})(jQuery);

var g;
$(document).ready(function() {
    
    $.getJSON('data/index.json', function(sessions) {
	
	_.each(sessions, function(session) {
	    $('#sessions').prepend(_.template('<p><a href="<%= session_url %>"><%= session_name %></a></p>', { session_name: session.split('/')[1].split('.')[0].replace('T', ' '), session_url: session }));
	});
	
	$('#sessions p a').click(function(e) {
	    e.preventDefault();
	    g.updateOptions({ file: $(this).attr('href') });
	});
	
	var w1 = $(window).width();
	var h1 = $(window).height();
	
	var w2 = $('#sessions').width();
	
	console.log(w1, h1, w2);
	
	$('#graph').width(w1-w2-100);
	$('#graph').height(h1-100);
	
	g = new Dygraph($('#graph').get(0), sessions[sessions.length-1], {
	    hideOverlayOnMouseOut: false,
	    displayAnnotations: true,
	    labelsSeparateLines: true,
	    legend: 'always',
	    drawXGrid: false
	});
    });
});
