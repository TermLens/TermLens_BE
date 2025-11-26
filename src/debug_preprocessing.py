from trafilatura import extract

from text_splitter import _normalize_block

# 원본 HTML/텍스트를 여기에 넣어 테스트합니다.
HTML_SOURCE = """
<html class=" responsive DesktopUI" lang="en"><head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
			<meta name="viewport" content="width=device-width,initial-scale=1">
		<meta name="theme-color" content="#171a21">
		<title>Steam Subscriber Agreement</title>
	<link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">

	
	
	<link href="https://store.akamai.steamstatic.com/public/shared/css/motiva_sans.css?v=4Vj7bvhvv_UL&amp;l=english&amp;_cdn=akamai" rel="stylesheet" type="text/css">
<link href="https://store.akamai.steamstatic.com/public/shared/css/shared_global.css?v=3n4z0aBsHfxR&amp;l=english&amp;_cdn=akamai" rel="stylesheet" type="text/css">
<link href="https://store.akamai.steamstatic.com/public/shared/css/buttons.css?v=u7ItYmj40jWH&amp;l=english&amp;_cdn=akamai" rel="stylesheet" type="text/css">
<link href="https://store.akamai.steamstatic.com/public/css/v6/store.css?v=PCSuCZpckZ1j&amp;l=english&amp;_cdn=akamai" rel="stylesheet" type="text/css">
<link href="https://store.akamai.steamstatic.com/public/css/styles_ssav5.css?v=w7kpfmpFD4ra&amp;l=english&amp;_cdn=akamai" rel="stylesheet" type="text/css">
<link href="https://store.akamai.steamstatic.com/public/shared/css/shared_responsive.css?v=1My8g2Hc4A9I&amp;l=english&amp;_cdn=akamai" rel="stylesheet" type="text/css">
<script type="text/javascript" src="https://store.akamai.steamstatic.com/public/shared/javascript/jquery-1.8.3.min.js?v=NXam5zydzNu8&amp;l=english&amp;_cdn=akamai"></script>
<script type="text/javascript">$J = jQuery.noConflict();</script><script type="text/javascript">VALVE_PUBLIC_PATH = "https:\/\/store.akamai.steamstatic.com\/public\/";</script><script type="text/javascript" src="https://store.akamai.steamstatic.com/public/shared/javascript/tooltip.js?v=LZHsOVauqTrm&amp;l=english&amp;_cdn=akamai"></script>

<script type="text/javascript" src="https://store.akamai.steamstatic.com/public/shared/javascript/shared_global.js?v=FXQ6SPy7N4Mq&amp;l=english&amp;_cdn=akamai"></script>

<script type="text/javascript" src="https://store.akamai.steamstatic.com/public/shared/javascript/auth_refresh.js?v=w6QbwI-5-j2S&amp;l=english&amp;_cdn=akamai"></script>

<script type="text/javascript" src="https://store.akamai.steamstatic.com/public/javascript/main.js?v=IBr21mD23BIS&amp;l=english&amp;_cdn=akamai"></script>

<script type="text/javascript" src="https://store.akamai.steamstatic.com/public/javascript/dynamicstore.js?v=SBXRiAJfiNfI&amp;l=english&amp;_cdn=akamai"></script>

<script type="text/javascript">
	var __PrototypePreserve=[];
	__PrototypePreserve[0] = Array.from;
	__PrototypePreserve[1] = Array.prototype.filter;
	__PrototypePreserve[2] = Array.prototype.flatMap;
	__PrototypePreserve[3] = Array.prototype.find;
	__PrototypePreserve[4] = Array.prototype.some;
	__PrototypePreserve[5] = Function.prototype.bind;
	__PrototypePreserve[6] = HTMLElement.prototype.scrollTo;
</script>
<script type="text/javascript" src="https://store.akamai.steamstatic.com/public/javascript/prototype-1.7.js?v=npJElBnrEO6W&amp;l=english&amp;_cdn=akamai"></script>
<script type="text/javascript">
	Array.from = __PrototypePreserve[0] || Array.from;
	Array.prototype.filter = __PrototypePreserve[1] || Array.prototype.filter;
	Array.prototype.flatMap = __PrototypePreserve[2] || Array.prototype.flatMap;
	Array.prototype.find = __PrototypePreserve[3] || Array.prototype.find;
	Array.prototype.some = __PrototypePreserve[4] || Array.prototype.some;
	Function.prototype.bind = __PrototypePreserve[5] || Function.prototype.bind;
	HTMLElement.prototype.scrollTo = __PrototypePreserve[6] || HTMLElement.prototype.scrollTo;
</script>
<script type="text/javascript">
	var __ScriptaculousPreserve=[];
	__ScriptaculousPreserve[0] = Array.from;
	__ScriptaculousPreserve[1] = Function.prototype.bind;
	__ScriptaculousPreserve[2] = HTMLElement.prototype.scrollTo;
</script>
<script type="text/javascript" src="https://store.akamai.steamstatic.com/public/javascript/scriptaculous/_combined.js?v=lz_99vci25ux&amp;l=english&amp;_cdn=akamai&amp;load=effects,controls,slider"></script>
<script type="text/javascript">
	Array.from = __ScriptaculousPreserve[0] || Array.from;
	Function.prototype.bind = __ScriptaculousPreserve[1] || Function.prototype.bind;
	HTMLElement.prototype.scrollTo = __ScriptaculousPreserve[2] || HTMLElement.prototype.scrollTo;
delete String['__parseStyleElement'];  Prototype.Browser.WebKit = true;</script>
<script type="text/javascript">Object.seal && [ Object, Array, String, Number ].map( function( builtin ) { Object.seal( builtin.prototype ); } );</script>
		<script type="text/javascript">
			document.addEventListener('DOMContentLoaded', function(event) {
				$J.data( document, 'x_readytime', new Date().getTime() );
				$J.data( document, 'x_oldref', GetNavCookie() );
				SetupTooltips( { tooltipCSSClass: 'store_tooltip'} );
		});
		</script><script type="text/javascript" src="https://store.akamai.steamstatic.com/public/shared/javascript/shared_responsive_adapter.js?v=cOPkuDRAsmuy&amp;l=english&amp;_cdn=akamai"></script>

						<meta name="twitter:card" content="summary_large_image">
			
	<meta name="twitter:site" content="@steam">

						<meta property="og:title" content="Steam Subscriber Agreement">
					<meta property="twitter:title" content="Steam Subscriber Agreement">
					<meta property="og:type" content="website">
					<meta property="fb:app_id" content="105386699540688">
					<meta property="og:site" content="Steam">
			
	
			<link rel="image_src" href="https://store.akamai.steamstatic.com/public/shared/images/responsive/steam_share_image.jpg">
		<meta property="og:image" content="https://store.akamai.steamstatic.com/public/shared/images/responsive/steam_share_image.jpg">
		<meta name="twitter:image" content="https://store.akamai.steamstatic.com/public/shared/images/responsive/steam_share_image.jpg">
					<meta property="og:image:secure" content="https://store.akamai.steamstatic.com/public/shared/images/responsive/steam_share_image.jpg">
				
	
	
	
	
	</head>
<body class="v6 widestore v7menu responsive_page ">


<div class="responsive_page_frame with_header">
						<div role="navigation" class="responsive_page_menu_ctn mainmenu" aria-label="Mobile Menu">
				<div class="responsive_page_menu" id="responsive_page_menu">
										<div class="mainmenu_contents">
						<div class="mainmenu_contents_items">
															<a class="menuitem" href="https://store.steampowered.com/login/?redir=subscriber_agreement%2F&amp;redir_ssl=1&amp;snr=1_subscriberagreement_SubscriberAgreement__global-header">
									Login								</a>
															<a class="menuitem supernav supernav_active" href="https://store.steampowered.com/?snr=1_subscriberagreement_SubscriberAgreement__global-responsive-menu" data-tooltip-type="selector" data-tooltip-content=".submenu_Store">
				Store			</a>
			<div class="submenu_Store" style="display: none;" data-submenuid="Store">
														<a class="submenuitem" href="https://store.steampowered.com/?snr=1_subscriberagreement_SubscriberAgreement__global-responsive-menu">
						Home											</a>
														<a class="submenuitem" href="https://store.steampowered.com/explore/?snr=1_subscriberagreement_SubscriberAgreement__global-responsive-menu">
						Discovery Queue											</a>
														<a class="submenuitem" href="https://steamcommunity.com/my/wishlist/">
						Wishlist											</a>
														<a class="submenuitem" href="https://store.steampowered.com/points/shop/?snr=1_subscriberagreement_SubscriberAgreement__global-responsive-menu">
						Points Shop											</a>
														<a class="submenuitem" href="https://store.steampowered.com/news/?snr=1_subscriberagreement_SubscriberAgreement__global-responsive-menu">
						News											</a>
														<a class="submenuitem" href="https://store.steampowered.com/stats/?snr=1_subscriberagreement_SubscriberAgreement__global-responsive-menu">
						Stats											</a>
							</div>
										<a class="menuitem supernav" href="https://steamcommunity.com/" data-tooltip-type="selector" data-tooltip-content=".submenu_Community">
				Community			</a>
			<div class="submenu_Community" style="display: none;" data-submenuid="Community">
														<a class="submenuitem" href="https://steamcommunity.com/">
						Home											</a>
														<a class="submenuitem" href="https://steamcommunity.com/discussions/">
						Discussions											</a>
														<a class="submenuitem" href="https://steamcommunity.com/workshop/">
						Workshop											</a>
														<a class="submenuitem" href="https://steamcommunity.com/market/">
						Market											</a>
														<a class="submenuitem" href="https://steamcommunity.com/?subsection=broadcasts">
						Broadcasts											</a>
							</div>
										<a class="menuitem " href="https://store.steampowered.com/about/?snr=1_subscriberagreement_SubscriberAgreement__global-responsive-menu">
				About			</a>
										<a class="menuitem " href="https://help.steampowered.com/en/">
				Support			</a>
			
							<div class="minor_menu_items">
																								<div class="menuitem change_language_action">
									Change language								</div>
																																	<a class="menuitem" href="https://store.steampowered.com/mobile" target="_blank" rel="noreferrer">Get the Steam Mobile App</a>
																									<div class="menuitem" role="link" onclick="Responsive_RequestDesktopView();">
										View desktop website									</div>
															</div>
						</div>
						<div class="mainmenu_footer_spacer  "></div>
						<div class="mainmenu_footer">
															<div class="mainmenu_footer_logo"><img src="https://store.akamai.steamstatic.com/public/shared/images/responsive/footerLogo_valve_new.png"></div>
								© Valve Corporation. All rights reserved. All trademarks are property of their respective owners in the US and other countries.								<span class="mainmenu_valve_links">
									<a href="https://store.steampowered.com/privacy_agreement/?snr=1_subscriberagreement_SubscriberAgreement__global-responsive-menu" target="_blank">Privacy Policy</a>
									&nbsp;| &nbsp;<a href="http://www.valvesoftware.com/legal.htm" target="_blank">Legal</a>
									&nbsp;| &nbsp;<a href="https://help.steampowered.com/faqs/view/10BB-D27A-6378-4436" target="_blank">Accessibility</a>
									&nbsp;| &nbsp;<a href="https://store.steampowered.com/subscriber_agreement/?snr=1_subscriberagreement_SubscriberAgreement__global-responsive-menu" target="_blank">Steam Subscriber Agreement</a>
									&nbsp;| &nbsp;<a href="https://store.steampowered.com/steam_refunds/?snr=1_subscriberagreement_SubscriberAgreement__global-responsive-menu" target="_blank">Refunds</a>
								</span>
													</div>
					</div>
									</div>
			</div>
		
		<div class="responsive_local_menu_tab"></div>

		<div class="responsive_page_menu_ctn localmenu">
			<div class="responsive_page_menu" id="responsive_page_local_menu" data-panel="{&quot;onOptionsActionDescription&quot;:&quot;Filter&quot;,&quot;onOptionsButton&quot;:&quot;Responsive_ToggleLocalMenu()&quot;,&quot;onCancelButton&quot;:&quot;Responsive_ToggleLocalMenu()&quot;}">
				<div class="localmenu_content" data-panel="{&quot;maintainY&quot;:true,&quot;bFocusRingRoot&quot;:true,&quot;flow-children&quot;:&quot;column&quot;}">
				</div>
			</div>
		</div>



					<div class="responsive_header">
				<div class="responsive_header_content _16qZv-fX6ub_MdNsHedaLI txwuWWnqKAsmG1rtZbvLo">
					<div id="responsive_menu_logo">
						<img src="https://store.akamai.steamstatic.com/public/shared/images/responsive/header_menu_hamburger.png" height="100%">
											</div>
					<div class="responsive_header_logo">
						<a href="https://store.steampowered.com/?snr=1_subscriberagreement_SubscriberAgreement__global-responsive-menu">
															<img src="https://store.akamai.steamstatic.com/public/shared/images/responsive/header_logo.png" height="36" border="0" alt="STEAM">
													</a>
					</div>
					<div class="responsive_header_react_target" data-featuretarget="store-menu-responsive-search"><div class="responsive_header_react_placeholder"></div><div class="_2uvYMNMk0jXWUkQtneMERT"><form class="_1KU9eASfov1GnFQRbyLIdR" role="search" method="GET" action="https://store.steampowered.com/search"><input type="hidden" value="1_subscriberagreement_SubscriberAgreement__7" name="snr"><div class="_2AD2O_FEWy7izR8sZZjjI6"><input class="_2tlUAG6WNyYFlk9caIiLj5" placeholder="Search the store" autocomplete="off" role="combobox" aria-expanded="false" aria-autocomplete="list" type="text" value="" name="term"></div><button class="_1Yo-ZsBr-KbVMyAMXEYszd" type="submit"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 18 18" fill="none" aria-label="Search"><path fill="currentColor" d="M13.8296 12.0786C14.8347 10.6321 15.2623 8.86133 15.0284 7.11496C14.7945 5.36859 13.9159 3.77313 12.5656 2.64269C11.2153 1.51224 9.49114 0.928708 7.73254 1.00696C5.97394 1.08522 4.30831 1.8196 3.06357 3.06552C1.81882 4.31144 1.08514 5.97864 1.00696 7.7389C0.928776 9.49916 1.51176 11.2249 2.64114 12.5765C3.77052 13.9281 5.36446 14.8075 7.10919 15.0417C8.85391 15.2758 10.623 14.8477 12.0682 13.8417L15.2185 17L15.3997 16.8187L16.8188 15.3982L17 15.2168L13.8296 12.0786ZM8.04222 12.5824C7.14643 12.5824 6.27075 12.3165 5.52593 11.8183C4.7811 11.3202 4.20058 10.6122 3.85777 9.78376C3.51497 8.95538 3.42528 8.04384 3.60004 7.16443C3.7748 6.28502 4.20616 5.47723 4.83958 4.84321C5.47301 4.20919 6.28004 3.77742 7.15862 3.60249C8.0372 3.42757 8.94787 3.51734 9.77548 3.86047C10.6031 4.2036 11.3104 4.78467 11.8081 5.5302C12.3058 6.27573 12.5714 7.15223 12.5714 8.04887C12.5714 9.25123 12.0943 10.4043 11.2449 11.2545C10.3955 12.1047 9.24344 12.5824 8.04222 12.5824V12.5824Z"></path></svg></button></form></div></div>				</div>
			</div>
		
		<div class="responsive_page_content_overlay">

		</div>

		<div class="responsive_fixonscroll_ctn nonresponsive_hidden ">
		</div>
	
	<div class="responsive_page_content">

		<div role="banner" id="global_header" data-panel="{&quot;flow-children&quot;:&quot;row&quot;}">
	<div class="content">
		<div class="logo">
			<span id="logo_holder">
									<a href="https://store.steampowered.com/?snr=1_subscriberagreement_SubscriberAgreement__global-header" aria-label="Link to the Steam Homepage">
						<img src="https://store.akamai.steamstatic.com/public/shared/images/header/logo_steam.svg?t=962016" width="176" height="44" alt="Link to the Steam Homepage">
					</a>
							</span>
		</div>

			<div role="navigation" class="supernav_container" aria-label="Global Menu">
								<a class="menuitem supernav supernav_active" href="https://store.steampowered.com/?snr=1_subscriberagreement_SubscriberAgreement__global-header" data-tooltip-type="selector" data-tooltip-content=".submenu_Store">
				STORE			</a>
			<div class="submenu_Store" style="display: none;" data-submenuid="Store">
														<a class="submenuitem" href="https://store.steampowered.com/?snr=1_subscriberagreement_SubscriberAgreement__global-header">
						Home											</a>
														<a class="submenuitem" href="https://store.steampowered.com/explore/?snr=1_subscriberagreement_SubscriberAgreement__global-header">
						Discovery Queue											</a>
														<a class="submenuitem" href="https://steamcommunity.com/my/wishlist/">
						Wishlist											</a>
														<a class="submenuitem" href="https://store.steampowered.com/points/shop/?snr=1_subscriberagreement_SubscriberAgreement__global-header">
						Points Shop											</a>
														<a class="submenuitem" href="https://store.steampowered.com/news/?snr=1_subscriberagreement_SubscriberAgreement__global-header">
						News											</a>
														<a class="submenuitem" href="https://store.steampowered.com/stats/?snr=1_subscriberagreement_SubscriberAgreement__global-header">
						Stats											</a>
							</div>
										<a class="menuitem supernav" href="https://steamcommunity.com/" data-tooltip-type="selector" data-tooltip-content=".submenu_Community">
				COMMUNITY			</a>
			<div class="submenu_Community" style="display: none;" data-submenuid="Community">
														<a class="submenuitem" href="https://steamcommunity.com/">
						Home											</a>
														<a class="submenuitem" href="https://steamcommunity.com/discussions/">
						Discussions											</a>
														<a class="submenuitem" href="https://steamcommunity.com/workshop/">
						Workshop											</a>
														<a class="submenuitem" href="https://steamcommunity.com/market/">
						Market											</a>
														<a class="submenuitem" href="https://steamcommunity.com/?subsection=broadcasts">
						Broadcasts											</a>
							</div>
										<a class="menuitem " href="https://store.steampowered.com/about/?snr=1_subscriberagreement_SubscriberAgreement__global-header">
				About			</a>
										<a class="menuitem " href="https://help.steampowered.com/en/">
				SUPPORT			</a>
				</div>
	<script type="text/javascript">
		jQuery(function($) {
			$('#global_header .supernav').v_tooltip({'location':'bottom', 'destroyWhenDone': false, 'tooltipClass': 'supernav_content', 'offsetY':-6, 'offsetX': 1, 'horizontalSnap': 4, 'tooltipParent': '#global_header .supernav_container', 'correctForScreenSize': false});
		});
	</script>

		<div id="global_actions">
			<div role="navigation" id="global_action_menu" aria-label="Account Menu">
									<a class="header_installsteam_btn header_installsteam_btn_green" href="https://store.steampowered.com/about/?snr=1_subscriberagreement_SubscriberAgreement__global-header">
						<div class="header_installsteam_btn_content">
							Install Steam						</div>
					</a>
				
				
									<a class="global_action_link" href="https://store.steampowered.com/login/?redir=subscriber_agreement%2F&amp;redir_ssl=1&amp;snr=1_subscriberagreement_SubscriberAgreement__global-header">login</a>
											&nbsp;|&nbsp;
						<span class="pulldown global_action_link" id="language_pulldown" onclick="ShowMenu( this, 'language_dropdown', 'right' );">language</span>
						<div class="popup_block_new" id="language_dropdown" style="display: none;">
							<div class="popup_body popup_menu">
																																					<a class="popup_menu_item tight" href="?l=schinese" onclick="ChangeLanguage( 'schinese' ); return false;">简体中文 (Simplified Chinese)</a>
																													<a class="popup_menu_item tight" href="?l=tchinese" onclick="ChangeLanguage( 'tchinese' ); return false;">繁體中文 (Traditional Chinese)</a>
																													<a class="popup_menu_item tight" href="?l=japanese" onclick="ChangeLanguage( 'japanese' ); return false;">日本語 (Japanese)</a>
																													<a class="popup_menu_item tight" href="?l=koreana" onclick="ChangeLanguage( 'koreana' ); return false;">한국어 (Korean)</a>
																													<a class="popup_menu_item tight" href="?l=thai" onclick="ChangeLanguage( 'thai' ); return false;">ไทย (Thai)</a>
																													<a class="popup_menu_item tight" href="?l=bulgarian" onclick="ChangeLanguage( 'bulgarian' ); return false;">Български (Bulgarian)</a>
																													<a class="popup_menu_item tight" href="?l=czech" onclick="ChangeLanguage( 'czech' ); return false;">Čeština (Czech)</a>
																													<a class="popup_menu_item tight" href="?l=danish" onclick="ChangeLanguage( 'danish' ); return false;">Dansk (Danish)</a>
																													<a class="popup_menu_item tight" href="?l=german" onclick="ChangeLanguage( 'german' ); return false;">Deutsch (German)</a>
																																							<a class="popup_menu_item tight" href="?l=spanish" onclick="ChangeLanguage( 'spanish' ); return false;">Español - España (Spanish - Spain)</a>
																													<a class="popup_menu_item tight" href="?l=latam" onclick="ChangeLanguage( 'latam' ); return false;">Español - Latinoamérica (Spanish - Latin America)</a>
																													<a class="popup_menu_item tight" href="?l=greek" onclick="ChangeLanguage( 'greek' ); return false;">Ελληνικά (Greek)</a>
																													<a class="popup_menu_item tight" href="?l=french" onclick="ChangeLanguage( 'french' ); return false;">Français (French)</a>
																													<a class="popup_menu_item tight" href="?l=italian" onclick="ChangeLanguage( 'italian' ); return false;">Italiano (Italian)</a>
																													<a class="popup_menu_item tight" href="?l=indonesian" onclick="ChangeLanguage( 'indonesian' ); return false;">Bahasa Indonesia (Indonesian)</a>
																													<a class="popup_menu_item tight" href="?l=hungarian" onclick="ChangeLanguage( 'hungarian' ); return false;">Magyar (Hungarian)</a>
																													<a class="popup_menu_item tight" href="?l=dutch" onclick="ChangeLanguage( 'dutch' ); return false;">Nederlands (Dutch)</a>
																													<a class="popup_menu_item tight" href="?l=norwegian" onclick="ChangeLanguage( 'norwegian' ); return false;">Norsk (Norwegian)</a>
																													<a class="popup_menu_item tight" href="?l=polish" onclick="ChangeLanguage( 'polish' ); return false;">Polski (Polish)</a>
																													<a class="popup_menu_item tight" href="?l=portuguese" onclick="ChangeLanguage( 'portuguese' ); return false;">Português (Portuguese - Portugal)</a>
																													<a class="popup_menu_item tight" href="?l=brazilian" onclick="ChangeLanguage( 'brazilian' ); return false;">Português - Brasil (Portuguese - Brazil)</a>
																													<a class="popup_menu_item tight" href="?l=romanian" onclick="ChangeLanguage( 'romanian' ); return false;">Română (Romanian)</a>
																													<a class="popup_menu_item tight" href="?l=russian" onclick="ChangeLanguage( 'russian' ); return false;">Русский (Russian)</a>
																													<a class="popup_menu_item tight" href="?l=finnish" onclick="ChangeLanguage( 'finnish' ); return false;">Suomi (Finnish)</a>
																													<a class="popup_menu_item tight" href="?l=swedish" onclick="ChangeLanguage( 'swedish' ); return false;">Svenska (Swedish)</a>
																													<a class="popup_menu_item tight" href="?l=turkish" onclick="ChangeLanguage( 'turkish' ); return false;">Türkçe (Turkish)</a>
																													<a class="popup_menu_item tight" href="?l=vietnamese" onclick="ChangeLanguage( 'vietnamese' ); return false;">Tiếng Việt (Vietnamese)</a>
																													<a class="popup_menu_item tight" href="?l=ukrainian" onclick="ChangeLanguage( 'ukrainian' ); return false;">Українська (Ukrainian)</a>
																									<a class="popup_menu_item tight" href="https://www.valvesoftware.com/en/contact?contact-person=Translation%20Team%20Feedback" target="_blank">Report a translation problem</a>
							</div>
						</div>
												</div>
					</div>
			</div>
</div>
<div class="_2QlYKhF-leHfMXFSiSshZC" data-featuretarget="store-menu-v7"><div class="PlaceholderInner"></div><div class="_2MzjSFlY9PHeDbUgNhjlOa"><div class="pzuGfMA6MeGlV2I3yY60c _1Zsv2NkXHxE5LTvs92Jqvd"><div class="h2B3SGR_w4RWdrnsRZEcD"><div class="_16jZ3HEbtaJTl80pQINN2Y Panel Focusable"><div class="_7FiqKP7fZJGltkwRxPG6s Panel Focusable" role="navigation" aria-label="Store menu"><div class="_1u2HkRz_FnAfR5OjfjexgF"><div class="_315CcpqsgdwaAwR3WiSlOq"><div class="_3CtcPWgZYR05CldoJ0Jkrx"><button class="_175B12uOwmeGBNcSaQFe-Z _3wlHWKFbgRAZPFtWEr65YT Focusable" aria-expanded="false" role="button"><div class="vj9hwW9u0MpjH7MVjjNw0">Browse<div class="_1-hPfsxjynE3demuqGmqf0"><div class="_3gaaE-cRfFWJdZcC8XMi0x"></div></div></div><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12" fill="none" role="presentation"><path fill="currentColor" fill-rule="evenodd" clip-rule="evenodd" d="M5.81026 6.36084L8.50899 3.66211L9.6875 4.84062L5.81026 8.71786L1.93302 4.84062L3.11153 3.66211L5.81026 6.36084Z"></path></svg></button><button class="_175B12uOwmeGBNcSaQFe-Z _3wlHWKFbgRAZPFtWEr65YT Focusable" aria-expanded="false" role="button"><div class="vj9hwW9u0MpjH7MVjjNw0">Recommendations<div class="_1-hPfsxjynE3demuqGmqf0"><div class="_3gaaE-cRfFWJdZcC8XMi0x"></div></div></div><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12" fill="none" role="presentation"><path fill="currentColor" fill-rule="evenodd" clip-rule="evenodd" d="M5.81026 6.36084L8.50899 3.66211L9.6875 4.84062L5.81026 8.71786L1.93302 4.84062L3.11153 3.66211L5.81026 6.36084Z"></path></svg></button><button class="_175B12uOwmeGBNcSaQFe-Z _3wlHWKFbgRAZPFtWEr65YT Focusable" aria-expanded="false" role="button"><div class="vj9hwW9u0MpjH7MVjjNw0">Categories<div class="_1-hPfsxjynE3demuqGmqf0"><div class="_3gaaE-cRfFWJdZcC8XMi0x"></div></div></div><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12" fill="none" role="presentation"><path fill="currentColor" fill-rule="evenodd" clip-rule="evenodd" d="M5.81026 6.36084L8.50899 3.66211L9.6875 4.84062L5.81026 8.71786L1.93302 4.84062L3.11153 3.66211L5.81026 6.36084Z"></path></svg></button><button class="_175B12uOwmeGBNcSaQFe-Z _3wlHWKFbgRAZPFtWEr65YT Focusable" aria-expanded="false" role="button"><div class="vj9hwW9u0MpjH7MVjjNw0">Hardware<div class="_1-hPfsxjynE3demuqGmqf0"><div class="_3gaaE-cRfFWJdZcC8XMi0x"></div></div></div><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12" fill="none" role="presentation"><path fill="currentColor" fill-rule="evenodd" clip-rule="evenodd" d="M5.81026 6.36084L8.50899 3.66211L9.6875 4.84062L5.81026 8.71786L1.93302 4.84062L3.11153 3.66211L5.81026 6.36084Z"></path></svg></button><button class="_175B12uOwmeGBNcSaQFe-Z _3wlHWKFbgRAZPFtWEr65YT Focusable" aria-expanded="false" role="button"><div class="vj9hwW9u0MpjH7MVjjNw0">Ways to Play<div class="_1-hPfsxjynE3demuqGmqf0"><div class="_3gaaE-cRfFWJdZcC8XMi0x"></div></div></div><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12" fill="none" role="presentation"><path fill="currentColor" fill-rule="evenodd" clip-rule="evenodd" d="M5.81026 6.36084L8.50899 3.66211L9.6875 4.84062L5.81026 8.71786L1.93302 4.84062L3.11153 3.66211L5.81026 6.36084Z"></path></svg></button></div><button class="_175B12uOwmeGBNcSaQFe-Z _3wlHWKFbgRAZPFtWEr65YT Focusable" aria-expanded="false" role="button"><div class="vj9hwW9u0MpjH7MVjjNw0">More<div class="_1-hPfsxjynE3demuqGmqf0"><div class="_3gaaE-cRfFWJdZcC8XMi0x"></div></div></div><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12" fill="none" role="presentation"><path fill="currentColor" fill-rule="evenodd" clip-rule="evenodd" d="M5.81026 6.36084L8.50899 3.66211L9.6875 4.84062L5.81026 8.71786L1.93302 4.84062L3.11153 3.66211L5.81026 6.36084Z"></path></svg></button></div><div class="WFyPwmwIjPaI784fImRbi"><div class="HWDmfh8Td_a8zxJu6tP0h"><div class="SWL3uBHWmdcYwUXE9yD0y" inert="" style="height: 0px; overflow: hidden; transition: height 100ms;"><div class="_2GxMhpm7OC2WWXN_wjgA78" id="searchSuggestions_«r0»"><a class="_2Cp17yynz2h_StEQZcNnqB" href="https://store.steampowered.com/search/?term=&amp;snr=1_7_15__advancedsearch"><span class="NOctYARrXun3C2m8ZOA3u">Advanced Search</span></a></div></div></div></div></div><div class="_1wn1lBlAzl3HMRqS1llwie"></div></div></div><div class="_19o1GB7ysfrWKLYpqZ6aXu"></div></div></div></div></div><div id="responsive_store_nav_ctn"></div><div id="responsive_store_nav_overlay" style="display:none"><div id="responsive_store_nav_overlay_ctn"></div><div id="responsive_store_nav_overlay_bottom"></div></div><div id="responsive_store_search_overlay" style="display:none"></div><div data-cart-banner-spot="1"></div>
		<div role="main" class="responsive_page_template_content" id="responsive_page_template_content" data-panel="{&quot;autoFocus&quot;:true}" style="--store-menu-overlap-height: 46px; --store-menu-floating-height: 46px;">

			<div id="application_config" style="display: none;" data-config="{&quot;EUNIVERSE&quot;:1,&quot;WEB_UNIVERSE&quot;:&quot;public&quot;,&quot;LANGUAGE&quot;:&quot;english&quot;,&quot;COUNTRY&quot;:&quot;KR&quot;,&quot;MEDIA_CDN_COMMUNITY_URL&quot;:&quot;https:\/\/cdn.akamai.steamstatic.com\/steamcommunity\/public\/&quot;,&quot;MEDIA_CDN_URL&quot;:&quot;https:\/\/cdn.akamai.steamstatic.com\/&quot;,&quot;VIDEO_CDN_URL&quot;:&quot;https:\/\/video.akamai.steamstatic.com\/&quot;,&quot;COMMUNITY_CDN_URL&quot;:&quot;https:\/\/community.akamai.steamstatic.com\/&quot;,&quot;COMMUNITY_CDN_ASSET_URL&quot;:&quot;https:\/\/cdn.akamai.steamstatic.com\/steamcommunity\/public\/assets\/&quot;,&quot;STORE_CDN_URL&quot;:&quot;https:\/\/store.akamai.steamstatic.com\/&quot;,&quot;PUBLIC_SHARED_URL&quot;:&quot;https:\/\/store.akamai.steamstatic.com\/public\/shared\/&quot;,&quot;COMMUNITY_BASE_URL&quot;:&quot;https:\/\/steamcommunity.com\/&quot;,&quot;CHAT_BASE_URL&quot;:&quot;https:\/\/steamcommunity.com\/&quot;,&quot;STORE_BASE_URL&quot;:&quot;https:\/\/store.steampowered.com\/&quot;,&quot;STORE_CHECKOUT_BASE_URL&quot;:&quot;https:\/\/checkout.steampowered.com\/&quot;,&quot;IMG_URL&quot;:&quot;https:\/\/store.akamai.steamstatic.com\/public\/images\/&quot;,&quot;STEAMTV_BASE_URL&quot;:&quot;https:\/\/steam.tv\/&quot;,&quot;HELP_BASE_URL&quot;:&quot;https:\/\/help.steampowered.com\/&quot;,&quot;PARTNER_BASE_URL&quot;:&quot;https:\/\/partner.steamgames.com\/&quot;,&quot;STATS_BASE_URL&quot;:&quot;https:\/\/partner.steampowered.com\/&quot;,&quot;INTERNAL_STATS_BASE_URL&quot;:&quot;https:\/\/steamstats.valve.org\/&quot;,&quot;IN_CLIENT&quot;:false,&quot;USE_POPUPS&quot;:false,&quot;STORE_ICON_BASE_URL&quot;:&quot;https:\/\/shared.akamai.steamstatic.com\/store_item_assets\/steam\/apps\/&quot;,&quot;STORE_ITEM_BASE_URL&quot;:&quot;https:\/\/shared.akamai.steamstatic.com\/store_item_assets\/&quot;,&quot;WEBAPI_BASE_URL&quot;:&quot;https:\/\/api.steampowered.com\/&quot;,&quot;TOKEN_URL&quot;:&quot;https:\/\/store.steampowered.com\/\/chat\/clientjstoken&quot;,&quot;BUILD_TIMESTAMP&quot;:1764112936,&quot;PAGE_TIMESTAMP&quot;:1764122588,&quot;IN_TENFOOT&quot;:false,&quot;IN_GAMEPADUI&quot;:false,&quot;IN_CHROMEOS&quot;:false,&quot;IN_MOBILE_WEBVIEW&quot;:false,&quot;PLATFORM&quot;:&quot;macos&quot;,&quot;BASE_URL_STORE_CDN_ASSETS&quot;:&quot;https:\/\/cdn.akamai.steamstatic.com\/store\/&quot;,&quot;EREALM&quot;:1,&quot;LOGIN_BASE_URL&quot;:&quot;https:\/\/login.steampowered.com\/&quot;,&quot;AVATAR_BASE_URL&quot;:&quot;https:\/\/avatars.akamai.steamstatic.com\/&quot;,&quot;FROM_WEB&quot;:true,&quot;WEBSITE_ID&quot;:&quot;Store&quot;,&quot;BASE_URL_SHARED_CDN&quot;:&quot;https:\/\/shared.akamai.steamstatic.com\/&quot;,&quot;CLAN_CDN_ASSET_URL&quot;:&quot;https:\/\/clan.akamai.steamstatic.com\/&quot;,&quot;COMMUNITY_ASSETS_BASE_URL&quot;:&quot;https:\/\/shared.akamai.steamstatic.com\/community_assets\/&quot;,&quot;SNR&quot;:&quot;1_subscriberagreement_SubscriberAgreement_&quot;}" data-userinfo="{&quot;logged_in&quot;:false,&quot;country_code&quot;:&quot;KR&quot;,&quot;excluded_content_descriptors&quot;:[3,4]}" data-hwinfo="{&quot;bSteamOS&quot;:false,&quot;bSteamDeck&quot;:false}" data-broadcastuser="{&quot;success&quot;:1,&quot;bHideStoreBroadcast&quot;:false}" data-store_user_config="{&quot;webapi_token&quot;:&quot;&quot;,&quot;shoppingcart&quot;:null,&quot;originating_navdata&quot;:{&quot;domain&quot;:&quot;store.steampowered.com&quot;,&quot;controller&quot;:&quot;direct-navigation&quot;,&quot;method&quot;:&quot;&quot;,&quot;submethod&quot;:&quot;&quot;,&quot;feature&quot;:&quot;&quot;,&quot;depth&quot;:0,&quot;countrycode&quot;:&quot;&quot;,&quot;webkey&quot;:null,&quot;is_client&quot;:false,&quot;curator_data&quot;:null,&quot;is_likely_bot&quot;:false,&quot;is_utm&quot;:false},&quot;wishlist_item_count&quot;:0}"></div><div id="application_root"><div class="_2uHYtSBLSS1MxFonkOXr0O"></div></div><script>window.g_wapit="";</script><link href="https://store.akamai.steamstatic.com/public/css/applications/store/main.css?v=-OpHNs5jJ5U_&amp;l=english&amp;_cdn=akamai" rel="stylesheet" type="text/css">
<script type="text/javascript" src="https://store.akamai.steamstatic.com/public/javascript/applications/store/manifest.js?v=2asKmCBkowT3&amp;l=english&amp;_cdn=akamai"></script>
<script type="text/javascript" src="https://store.akamai.steamstatic.com/public/javascript/applications/store/libraries~b28b7af69.js?v=FInPE8IrzLqw&amp;l=english&amp;_cdn=akamai"></script>
<script type="text/javascript" src="https://store.akamai.steamstatic.com/public/javascript/applications/store/main.js?v=Z30MdHOCPNXk&amp;l=english&amp;_cdn=akamai"></script>
<script type="text/javascript">
	var g_AccountID = 0;
	var g_Languages = ["english"];
	var g_sessionID = "714fc310b4f2e12bb71c4b58";
	var g_ServerTime = 1764122588;
	var g_bUseNewCartAPI = true;

	$J( InitMiniprofileHovers( 'https%3A%2F%2Fstore.steampowered.com%2F' ) );

	
	if ( typeof GStoreItemData != 'undefined' )
	{
		GStoreItemData.AddNavParams({
			__page_default: "1_subscriberagreement_SubscriberAgreement_",
			__page_default_obj: {"domain":"store.steampowered.com","controller":"subscriberagreement","method":"SubscriberAgreement","submethod":"","feature":null,"depth":null,"countrycode":"KR","webkey":null,"is_client":false,"curator_data":null,"is_likely_bot":false,"is_utm":null},
			__originating_obj: {"domain":"store.steampowered.com","controller":"direct-navigation","method":"","submethod":"","feature":"","depth":0,"countrycode":"","webkey":null,"is_client":false,"curator_data":null,"is_likely_bot":false,"is_utm":false},
			storemenu_recommendedtags: "1_subscriberagreement_SubscriberAgreement__17"		});
	}

	if ( typeof GDynamicStore != 'undefined' )
	{
		GDynamicStore.Init(0, false, "", {"primary_language":null,"secondary_languages":null,"platform_windows":null,"platform_mac":null,"platform_linux":null,"timestamp_updated":null,"hide_store_broadcast":null,"review_score_preference":null,"timestamp_content_descriptor_preferences_updated":null,"provide_deck_feedback":null,"additional_languages":null}, 'KR',
			{"bNoDefaultDescriptors":false});
		GStoreItemData.SetCurrencyFormatter(function( nValueInCents, bWholeUnitsOnly ) { var fmt = function( nValueInCents, bWholeUnitsOnly ) {	var format = v_numberformat( nValueInCents / 100, bWholeUnitsOnly ? 0 : 2, ".", ",");format = format.replace( ".00", '' ); return format; };var strNegativeSymbol = '';return strNegativeSymbol + "\u20a9 " + fmt( nValueInCents, bWholeUnitsOnly );});
		GStoreItemData.SetCurrencyMinPriceIncrement(1000);
	}
</script>
<div id="main">

	<div id="main_content">
		<div class="page_title_area">
			<div class="breadcrumbs">
				<div class="blockbg">
					<a href="https://store.steampowered.com/">Home</a>
				</div>
				<div style="clear: left;"></div>
			</div>
			<div class="page_name">
				<div class="blockbg">
					Steam Subscriber Agreement				</div>
				<div style="clear: left;"></div>
			</div>
		</div>

		<div id="ssa_box">
			<div id="languages">
									<a href="https://store.steampowered.com/subscriber_agreement/english/"><img src="https://store.akamai.steamstatic.com/public/images/languageflags/english.gif" border="0"></a>
									<a href="https://store.steampowered.com/subscriber_agreement/spanish/"><img src="https://store.akamai.steamstatic.com/public/images/languageflags/spanish.gif" border="0"></a>
									<a href="https://store.steampowered.com/subscriber_agreement/french/"><img src="https://store.akamai.steamstatic.com/public/images/languageflags/french.gif" border="0"></a>
									<a href="https://store.steampowered.com/subscriber_agreement/german/"><img src="https://store.akamai.steamstatic.com/public/images/languageflags/german.gif" border="0"></a>
									<a href="https://store.steampowered.com/subscriber_agreement/italian/"><img src="https://store.akamai.steamstatic.com/public/images/languageflags/italian.gif" border="0"></a>
									<a href="https://store.steampowered.com/subscriber_agreement/russian/"><img src="https://store.akamai.steamstatic.com/public/images/languageflags/russian.gif" border="0"></a>
									<a href="https://store.steampowered.com/subscriber_agreement/japanese/"><img src="https://store.akamai.steamstatic.com/public/images/languageflags/japanese.gif" border="0"></a>
									<a href="https://store.steampowered.com/subscriber_agreement/portuguese/"><img src="https://store.akamai.steamstatic.com/public/images/languageflags/portuguese.gif" border="0"></a>
									<a href="https://store.steampowered.com/subscriber_agreement/brazilian/"><img src="https://store.akamai.steamstatic.com/public/images/languageflags/brazilian.gif" border="0"></a>
									<a href="https://store.steampowered.com/subscriber_agreement/polish/"><img src="https://store.akamai.steamstatic.com/public/images/languageflags/polish.gif" border="0"></a>
							</div>
			<div id="ssa_body">
	<h3>STEAM® SUBSCRIBER AGREEMENT</h3><br>
	<p><a name="0"></a>Table of contents:
		</p><ol style="margin-left: 13px;">
			<li><a href="#1">Registration as a subscriber; application of terms to you; your account; conclusion of agreements</a></li>
			<li><a href="#2">Licenses</a></li>
			<li><a href="#3">Billing, payment and other subscriptions</a></li>
			<li><a href="#4">Online conduct, cheating and automation</a></li>
			<li><a href="#5">Third-party content</a></li>
			<li><a href="#6">User generated content</a></li>
			<li><a href="#7">Disclaimers; limitation of liability; no guarantees; limited warranty &amp; agreement</a></li>
			<li><a href="#8">Amendments to this agreement</a></li>
			<li><a href="#9">Term and termination</a></li>
			<li><a href="#10">Applicable law/jurisdiction</a></li>
			<li><a href="#11">Miscellaneous</a></li>
		</ol>
	<p></p>
	
	<p>This Steam Subscriber Agreement ("Agreement") is a legal document that explains your rights and obligations as a subscriber of Steam from Valve Corporation, a corporation under the laws of the State of Washington, with its registered office at 10400 NE 4th St., Bellevue, WA 98004, United States, registered with the Washington Secretary of State under number 60 22 90 773, VAT ID No. EU 8260 00671 ("Valve"). Please read it carefully.</p>	
	
	<a name="1"></a>
	<p>1. REGISTRATION AS A SUBSCRIBER; APPLICATION OF TERMS TO YOU; YOUR ACCOUNT, ACCEPTANCE OF AGREEMENTS<a href="#0" style="text-decoration: none;"><small style="color: #666;">  ⏶</small></a></p>
		<p>Steam is an online service offered by Valve.</p>
		<p>You become a subscriber of Steam ("Subscriber") by completing the registration of a Steam user account.  This Agreement takes effect as soon as you indicate your acceptance of these terms.  You may not become a Subscriber if you are under the age of 13.  Steam is not intended for children under 13 and Valve will not knowingly collect personal information from children under the age of 13. Additional age restrictions may apply in your country.</p>
			<p>A. Contracting Party</p>
				<p>For any interaction with Steam your contractual relationship is with Valve. Except as otherwise indicated herein or at the time of the transaction (such as in the case of a transaction with another Subscriber in a Subscription Marketplace), any transactions for Subscriptions (as defined below) you make on Steam are being made from Valve.</p>
			<p>B. Hardware, Subscriptions; Content and Services</p>
				<p>As a Subscriber you may obtain access to certain services, software and content available to Subscribers or purchase certain Hardware (as defined below) on Steam.  The Steam client software and any other software, content, and updates you download or access via Steam, including but not limited to Valve or third-party video games and in-game content, software associated with Hardware and any virtual items you may acquire in a Subscription Marketplace are referred to in this Agreement as "Content and Services;" the rights to access and/or use any Content and Services accessible through Steam are referred to in this Agreement as "Subscriptions."</p>
				<p>Each Subscription allows you to access particular Content and Services.  Some Subscriptions may impose additional terms specific to that Subscription ("Subscription Terms") (for example, an end user license agreement specific to a particular game, or terms of use specific to a particular product or feature of Steam).  Also, additional terms (for example, payment and billing procedures) may be posted on <a target="_new" href="http://www.steampowered.com">http://www.steampowered.com</a> or within the Steam service ("Rules of Use"). Rules of Use include the Steam Online Conduct Rules <a target="_new" href="http://steampowered.com/index.php?area=online_conduct">http://steampowered.com/index.php?area=online_conduct</a> and the Steam Refund Policy <a target="_new" href="http://store.steampowered.com/steam_refunds">http://store.steampowered.com/steam_refunds</a>.  The Subscription Terms, the Rules of Use, and the Valve Privacy Policy (which can be found at <a target="_new" href="http://www.valvesoftware.com/privacy.htm">http://www.valvesoftware.com/privacy.htm</a>) are binding on you once you indicate your acceptance of them or of this Agreement, or otherwise become bound by them as described in Section 8 (Amendments to this Agreement).</p>
			<p>C. Your Account</p>
				<p>When you complete Steam’s registration process, you create a Steam account ("Account"). Your Account may also include billing information you provide to Valve for transactions concerning Subscriptions, Content and Services and the purchase of any physical goods through Steam (“Hardware”). You may not reveal, share or otherwise allow others to use your password or Account except as otherwise specifically authorized by Valve. You are responsible for the confidentiality of your login and password and for the security of your computer system. Valve is not responsible for the use of your password and Account or for all of the communication and activity on Steam that results from use of your login name and password by you, or  by any person to whom you may have intentionally or by negligence disclosed your login and/or password in violation of this confidentiality provision. Unless it results from Valve’s negligence or fault, Valve is not responsible for the use of your Account by a person who fraudulently used your login and password without your permission. If you believe that the confidentiality of your login and/or password may have been compromised, you must notify Valve via the support form (<a target="_new" href="https://support.steampowered.com/newticket.php">https://support.steampowered.com/newticket.php</a>) without any delay.</p>
				<p>Your Account, including any information pertaining to it (e.g.: contact information, billing information, Account history and Subscriptions, etc.), is strictly personal. You may therefore not sell or charge others for the right to use your Account, or otherwise transfer your Account, nor may you sell, charge others for the right to use, or transfer any Subscriptions other than if and as expressly permitted by this Agreement (including any Subscription Terms or Rules of Use) or as otherwise specifically permitted by Valve. Furthermore, you must not use your Account to enable a violation of this Agreement by others, such as through their commercial use of Steam Content and Services. </p>
			<p>D. Acceptance of Agreements</p>
				<p>Your order through Steam is an offer to Valve to agree on the delivery of the ordered Subscriptions, Content and Services and/or Hardware (the “Product(s)”) in exchange for the listed price.</p>
				<p>When you place an order on Steam, we will send you a message confirming receipt of your order and containing the details of your order (the “Order Confirmation”). The Order Confirmation is acknowledgement that we have received your order and does not confirm acceptance of your offer to enter into an agreement.</p>
				<p>In the case of Content and Services, we accept your offer, and conclude the agreement with you, by confirming the transaction and making the Content and Services available to you or, in the case of pre-orders, only by confirming the transaction to you and deducting the applicable price from your payment method.</p>
				<p>In the case of Hardware, we only accept your offer, and conclude the transaction for an item ordered by you, when we dispatch the Hardware to you and send e-mail confirming to you that we've dispatched the Hardware to you (the "Dispatch Confirmation"). If your order is dispatched in more than one package, you may receive a separate Dispatch Confirmation for each package, and each Dispatch Confirmation and corresponding dispatch will conclude a separate contract of sale between us for the Hardware specified in that Dispatch Confirmation. Any Hardware delivered to you remains property of Valve until payment has been fully made.</p>
				<p>You consent to receiving sales invoices electronically.</p>
			<p>E. Payment Processing</p>
				<p>Payment processing related to Content and Services and/or Hardware purchased on Steam is performed by either Valve Corporation directly or by Valve’s fully owned subsidiary Valve GmbH on behalf of Valve Corporation depending on the type of payment method used.  If your card was issued outside the United States, your payment may be processed via a European acquirer by Valve GmbH on behalf of Valve Corporation. For any other type of purchases, payment will be collected by Valve Corporation directly. In any case, delivery of Content and Services as well as Hardware is performed by Valve Corporation.</p>
	
	<a name="2"></a>
	<p>2. LICENSES<a href="#0" style="text-decoration: none;"><small style="color: #666;">  ⏶</small></a></p>
			<p>A. General Content and Services License</p>
				<p>Steam and your Subscription(s) require the download and installation of Content and Services onto your computer.  Valve hereby grants, and you accept, a non-exclusive license and right, to use the Content and Services for your personal, non-commercial use (except where commercial use is expressly allowed herein or in the applicable Subscription Terms). This license ends upon termination of (a) this Agreement or (b) a Subscription that includes the license.  The Content and Services are licensed, not sold. Your license confers no title or ownership in the Content and Services.  To make use of the Content and Services, you must have a Steam Account and you may be required to be running the Steam client and maintaining a connection to the Internet.  </p>
				<p>For reasons that include, without limitation, system security, stability, and multiplayer interoperability, Valve may need to automatically update, pre-load, create new versions of or otherwise enhance the Content and Services and accordingly, the system requirements to use the Content and Services may change over time.</p>
				<p>You consent to such automatic updating.  You understand that this Agreement (including applicable Subscription Terms) does not entitle you to future updates (unless to the extent required by applicable law), new versions or other enhancements of the Content and Services associated with a particular Subscription, although Valve may choose to provide such updates, etc. in its sole discretion.</p>
			<p>B. Beta Software License</p>
				<p>Valve may from time to time make software accessible to you via Steam prior to the general commercial release of such software ("Beta Software"). You are not required to use Beta Software, but if Valve offers it, you may elect to use it under the following terms. Beta Software will be deemed to consist of Content and Services, and each item of Beta Software provided will be deemed a Subscription for such Beta Software, with the following provisions specific to Beta Software:</p>
		<p>
			</p><ul>
				<li>Your right to use the Beta Software may be limited in time, and may be subject to additional Subscription Terms;<br>
				</li><li>Valve or any Valve affiliate may request or require that you provide suggestions, feedback, or data regarding your use of the Beta Software, which will be deemed User Generated Content under Section 6 (User Generated Content) below; and<br>
				</li><li>In addition to the waivers and limitations of liability for all Software under Section 7 (Disclaimers; Limitations on Liability; No Guarantees; Limited Warranty &amp; Agreement) below as applicable, you specifically acknowledge that Beta Software is only released for testing and improvement purposes, in particular to provide Valve with feedback on the quality and usability of the Beta Software, and therefore contains errors and is not final. If you decide to install and/or use Beta Software, you shall only use it in compliance with its purposes, i.e. for testing and improvement purposes, in compliance with system requirements specifically intended for each Beta Software and in any case not on a system or for purposes where the malfunction of the Beta Software can cause any kind of damage. In particular, maintain full backups of any system that you choose to install Beta Software on.
			</li></ul>
		<p></p>
			<p>C. License to Use Valve Developer Tools</p>
				<p>Your Subscription(s) may include access to various Valve tools that can be used to create content ("Developer Tools").  Some examples include:  the Valve software development kit (the "SDK") for a version of the computer game engine known as "Source" (the "Source Engine") and the associated Valve Hammer editor, The Source® Filmmaker Software, or in-game tools through which you can edit or create derivative works of a Valve game.  Particular Developer Tools (for example, The Source® Filmmaker Software) may be distributed with separate Subscription Terms that are different from the rules set forth in this Section.  Except as set forth in any separate Subscription Terms applicable to the use of a particular Developer Tool, you may use the Developer Tools, and you may use, reproduce, publish, perform, display and distribute any content you create using the Developer Tools, however you wish, but solely on a non-commercial basis.</p>
				<p>If you would like to use the Source Engine SDK or other Valve Developer Tools for commercial use, please contact Valve at sourceengine@valvesoftware.com.</p>
			<p>D. License to Use Valve Game Content in Fan Art.</p>
				<p>Valve appreciates the community of Subscribers that creates fan art, fan fiction, and audio-visual works that reference Valve games ("Fan Art").  You may incorporate content from Valve games into your Fan Art.  Except as otherwise set forth in this Section or in any Subscription Terms, you may use, reproduce, publish, perform, display and distribute Fan Art that incorporates content from Valve games however you wish, but solely on a non-commercial basis.</p> 
				<p>If you incorporate any third-party content in any Fan Art, you must be sure to obtain all necessary rights from the owner of that content.</p>
				<p>Commercial use of some Valve game content is permitted via features such as Steam Workshop or a Steam Subscription Marketplace.  Terms applicable to that use are set forth in Sections 3.D. and 6.B. below and in any Subscription Terms provided for those features.</p>
				<p>To view the Valve video policy containing additional terms covering the use of audio-visual works incorporating Valve intellectual property or created with The Source® Filmmaker Software, please click here: <a target="_new" href="http://www.valvesoftware.com/videopolicy.html">http://www.valvesoftware.com/videopolicy.html</a></p>
			<p>E. License to Use Valve Dedicated Server Software </p>
				<p>Your Subscription(s) may contain access to the Valve Dedicated Server Software. If so, you may use the Valve Dedicated Server Software on an unlimited number of computers for the purpose of hosting online multiplayer games of Valve products. If you wish to operate the Valve Dedicated Server Software, you will be solely responsible for procuring any Internet access, bandwidth, or hardware for such activities and will bear all costs associated with your use.</p>
			<p>F. Ownership of Content and Services</p>
				<p>All title, ownership rights and intellectual property rights in and to the Content and Services and any and all copies thereof, are owned by Valve and/or its or its affiliates’ licensors. All rights are reserved, except as expressly stated herein. The Content and Services are protected by copyright laws, international copyright treaties and conventions and other laws. The Content and Services contain certain licensed materials and Valve’s and its affiliates’ licensors may protect their rights in the event of any violation of this Agreement.</p>
			<p>G. Restrictions on Use of Content and Services</p>
				<p>You may not use the Content and Services for any purpose other than the permitted access to Steam and your Subscriptions, and to make personal, non-commercial use of your Subscriptions, except as otherwise permitted by this Agreement or applicable Subscription Terms.  Except as otherwise permitted under this Agreement (including any Subscription Terms or Rules of Use), or under applicable law notwithstanding these restrictions, you may not, in whole or in part, copy, photocopy, reproduce, publish, distribute, translate, reverse engineer, derive source code from, modify, disassemble, decompile, create derivative works based on, or remove any proprietary notices or labels from the Content and Services or any software accessed via Steam without the prior consent, in writing, of Valve.</p>
				<p>You are entitled to use the Content and Services for your own personal use, but you are not entitled to: (i) sell, grant a security interest in or transfer reproductions of the Content and Services to other parties in any way, nor to rent, lease or license the Content and Services to others without the prior written consent of Valve, except to the extent expressly permitted elsewhere in this Agreement (including any Subscription Terms or Rules of Use); (ii) host or provide matchmaking services for the Content and Services or emulate or redirect the communication protocols used by Valve in any network feature of the Content and Services, through protocol emulation, tunneling, modifying or adding components to the Content and Services, use of a utility program or any other techniques now known or hereafter developed, for any purpose including, but not limited to network play over the Internet, network play utilizing commercial or non-commercial gaming networks or as part of content aggregation networks, websites or services, without the prior written consent of Valve; or (iii) exploit the Content and Services or any of its parts for any commercial purpose, except as expressly permitted elsewhere in this Agreement (including any Subscription Terms or Rules of Use). </p>
	
	<a name="3"></a>
	<p>3. BILLING, PAYMENT AND OTHER SUBSCRIPTIONS<a href="#0" style="text-decoration: none;"><small style="color: #666;">  ⏶</small></a></p>
		<p>All charges incurred on Steam, and all purchases made with the Steam Wallet, are payable in advance and final, except as described in Sections 3.I and 7 below.</p>
			<p>A. Payment Authorization</p>
				<p>When you provide payment information to Valve or to one of its payment processors, you represent to Valve that you are the authorized user of the card, PIN, key or account associated with that payment, and you authorize Valve to charge your credit card or to process your payment with the chosen third-party payment processor for any Subscription, Steam Wallet funds, Hardware or other fees incurred by you.</p>
				<p>For Subscriptions ordered based on an agreed usage period, where recurring payments are made in exchange for continued use ("Recurring Payment Subscriptions"), by continuing to use the Recurring Payment Subscription you agree and reaffirm that Valve is authorized to charge your credit card (or your Steam Wallet, if funded), or to process your payment with any other applicable third-party payment processor, for any applicable recurring payment amounts. If you have ordered any Recurring Payment Subscriptions, you agree to notify Valve promptly of any changes to your credit card account number, its expiration date and/or your billing address, or your PayPal or other payment account number, and you agree to notify Valve promptly if your credit card or PayPal or other payment account expires or is cancelled for any reason.</p>
				<p>If your use of Steam or your purchase of Hardware on Steam is subject to any type of use or sales tax, then Valve may also charge you for those taxes, in addition to the Subscription or other fees published in the Rules of Use. All fees on Steam in the European Union and the United Kingdom include the EU or UK VAT ("VAT") tax. VAT amounts collected by Valve reflect VAT due on the value of any Content and Services, Hardware or Subscription.</p>
				<p>You agree that you will not use IP proxying or other methods to disguise the place of your residence, whether to circumvent geographical restrictions on game content, to order or purchase at pricing not applicable to your geography, or for any other purpose.  If you do this, Valve may terminate your access to your Account.</p>
			<p>B. Responsibility for Charges Associated With Your Account</p>
				<p>As the Account holder, you are responsible for all charges incurred, including applicable taxes, and all orders or purchases made by you or anyone that uses your Account, including your family or friends. If you cancel your Account, Valve reserves the right to collect fees, surcharges or costs incurred before cancellation. Any delinquent or unpaid Accounts must be settled before Valve will allow you to register again.</p>
			<p>C. Steam Wallet</p>
				<p>Steam may make available an account balance associated with your Account (the "Steam Wallet").  The Steam Wallet is neither a bank account nor any kind of payment instrument. It functions as a prepaid balance to order Content and Services. You may place funds in your Steam Wallet up to a maximum amount determined by Valve, by credit card, prepaid card, promotional code, or any other payment method accepted by Steam.  Within any twenty-four (24) hour period, the total amount stored in your Steam Wallet plus the total amount spent out of your Steam Wallet, in the aggregate, may not exceed US$2,000 or its equivalent in your applicable local currency -- attempted deposits into your Steam Wallet that exceed this threshold may not be credited to your Steam Wallet until your activity falls below this threshold. Valve may change or impose different Steam Wallet balance and usage limits from time to time.</p>
				<p>You will be notified by e-mail of any change to the Steam Wallet balance and usage limits within sixty (60) calendar days before the entry into force of the change. Your continued use of your Steam Account more than thirty (30) calendar days after the entry into force of the changes will constitute your acceptance of the changes. If you don’t agree to the changes, your only remedy is to terminate your Steam Account or to cease use of your Steam Wallet. Valve shall not have any obligation to refund any credits remaining on your Steam Wallet in this case.</p>
				<p>You may use Steam Wallet funds to order Subscriptions, including by making in-game orders where Steam Wallet transactions are enabled, and purchase Hardware. Subject to Section 3.I, funds added to the Steam Wallet are non-refundable and non-transferable. Steam Wallet funds do not constitute a personal property right, have no value outside Steam and can only be used to order Subscriptions and related content via Steam (including but not limited to games and other applications offered through the Steam Store, or in a Steam Subscription Marketplace) and Hardware. Steam Wallet funds have no cash value and are not exchangeable for cash. Steam Wallet funds that are deemed unclaimed property may be turned over to the applicable authority.</p>
			<p>D. Trading and Transactions of Subscriptions Between Subscribers</p>
				<p>Steam may include  one or more features or sites that allow Subscribers to acquire or dispose of certain types of Subscriptions (for example, license rights to virtual items) with, to or from other Subscribers ("Subscription Marketplaces"). The Steam Community Market and the Steam Trading functionality are both examples of Subscription Marketplaces. By using or participating in Subscription Marketplaces, you authorize Valve, on its own behalf or as an agent or licensee of any third-party creator or publisher of the applicable Subscriptions in your Account, to transfer those Subscriptions from your Account in order to give effect to any transaction you make.</p>
				<p>Valve may charge a fee for transactions in a Subscription Marketplace.  Any fees will be disclosed to you prior to the completion of the transaction.</p>
				<p>Valve collects sales tax/VAT/GST/etc. for transactions in a Subscription Marketplace as required by law. You should consult with a tax specialist to determine your tax liability in connection with your activities in any Subscription Marketplace.</p>
				<p>You understand and acknowledge that Valve does not have any obligation to provide or maintain any Subscription Marketplace. Valve may decide to cease operation of any Subscription Marketplace, change the fees that it charges or change the terms or features of the Steam Subscription Marketplace. You will be notified of any substantial change to the terms or availability of the Subscription Marketplace in a timely fashion before the entry into force of the change, except in cases of force majeure, Subscriber's fault or third party event outside of Valve's control.</p>
				<p>You also understand and acknowledge that Subscriptions acquired in any Subscription Marketplace are license rights, that you have no ownership interest in such Subscriptions, and that Valve does not recognize any transfers of Subscriptions (including transfers by operation of law) that are made outside of Steam.</p>
			<p>E. Retail Purchase</p>
				<p>Valve may offer or require a Subscription for purchasers of retail packaged product versions or OEM versions of Valve products. The "CD-Key" or "Product Key" accompanying such versions is used to activate your Subscription. Further instructions will be provided along with the respective product.</p>
			<p>F. Steam Authorized Resellers</p>
				<p>You may order a Subscription through an authorized reseller of Valve. The "Product Key" accompanying such order will be used to activate your Subscription. Further instructions will be provided along with the respective product. If you order a Subscription from an authorized reseller of Valve, you agree to direct all questions regarding the Product Key to that reseller.</p>
			<p>G. Free Subscriptions</p>
				<p>In some cases, Valve may offer a free Subscription to certain Content and Services. As with all Subscriptions, you are always responsible for any Internet service provider, telephone, and other connection fees that you may incur when using Steam, even when Valve offers a free Subscription.</p>
			<p>H. Third-Party Sites</p>
				<p>Steam may provide links to other third-party sites. Some of these sites may charge separate fees, which are not included in and are in addition to any Subscription or other fees that you may pay to Valve. Steam may also provide access to third-party vendors, who provide content, goods and/or services on Steam or the Internet. Any separate charges or obligations you incur in your dealings with these third parties are your responsibility. Valve makes no representations or warranties, either express or implied, regarding any third party site. In particular, Valve makes no representation or warranty that any service or subscription offered via third-party vendors will not change or be suspended or terminated.</p>
			<p>I. Refunds and Right of Withdrawal</p>
				<p>Without prejudice to any statutory rights you may have, you can request a refund for your orders or purchases on Steam in accordance with the terms of Valve’s Refund Policy <a target="_new" href="http://store.steampowered.com/steam_refunds/">http://store.steampowered.com/steam_refunds/</a>.</p>
				<p>For European Union and United Kingdom consumers:</p>
				<p>EU and UK law provides a statutory right to withdraw from certain contracts for physical merchandise and for the order of digital content. You can find more information about the extent of your statutory right to withdraw and the ways you can exercise it on this page: <a target="_new" href="https://support.steampowered.com/kb_article.php?ref=8620-QYAL-4516">https://support.steampowered.com/kb_article.php?ref=8620-QYAL-4516</a>.</p>
	
	<a name="4"></a>
	<p>4. ONLINE CONDUCT, CHEATING AND AUTOMATION<a href="#0" style="text-decoration: none;"><small style="color: #666;">  ⏶</small></a></p>
		<p>A. Online Conduct</p>
		<p>Your online conduct and interaction with other Subscribers must comply with the Steam Online Conduct Rules, to be found at <a target="_new" href="http://steampowered.com/index.php?area=online_conduct">http://steampowered.com/index.php?area=online_conduct</a>. Depending on terms of use imposed by third parties who host particular games or other services, additional requirements may also be provided in the Subscription Terms applicable to a particular Subscription.</p>
		<p>B. Cheating</p>
		<p>Steam and the Content and Services may include functionality designed to identify software or hardware processes or functionality that may give a player an unfair competitive advantage when playing multiplayer versions of any Content and Services or modifications of Content and Services ("Cheats"). You agree that you will not create Cheats or assist third parties in any way to create or use Cheats. You agree that you will not directly or indirectly disable, circumvent, or otherwise interfere with the operation of software designed to prevent or report the use of Cheats.</p>
		<p>You agree that you will not tamper with the execution of Steam or Content and Services unless otherwise authorized by Valve. 
		You may not use Cheats, mods, hacks, or any other unauthorized third-party software, to modify any Subscription Marketplace process, the process of Steam account creation or otherwise in interacting with or controlling the processes or user interface of Steam Content and Services, except to the degree expressly permitted.</p>
		<p>C. Automation</p>
		<p>You may not use any form of scripts, bots, macros, or other non-human-controlled systems (“Automation”) to interact with Content and Services on Steam in any manner, including but not limited to:</p>
		<ul>
			<li>Automating the Steam account creation process,</li>
			<li>Faking gameplay statistics (e.g., inflated wins or losses, XP, playtime),</li>
			<li>Earning rewards or progress without genuine user input,</li>
			<li>Participating in adjudication systems (like peer reviews or “overwatch”) through automated means, including influencing outcomes or reporting users by scripted action rather than informed judgment.</li>
		</ul>
		<p>D. Enforcement</p>
		<p>We may enforce this provision using both automated detection methods and human review, in accordance with our policies and applicable law. </p>
		<p>Further, you acknowledge and agree that any host of an online multiplayer game distributed through Steam ("External Host") may report your use of Cheats, unauthorized process tampering or Automation to Valve, and Valve may communicate your history of use thereof to External Hosts within the boundaries of the Steam Privacy Policy.</p>
		<p>Valve may restrict or terminate your Account(s) or a particular Subscription for any conduct or activity that is illegal, constitutes a Cheat or Automation or breaches the Steam Online Conduct Rules. You acknowledge that Valve is not required to provide you notice before terminating your Subscription(s) and/or Account.</p>
	
	<a name="5"></a>
	<p>5. THIRD-PARTY CONTENT<a href="#0" style="text-decoration: none;"><small style="color: #666;">  ⏶</small></a></p>
		<p>In regard to all Subscriptions, Content and Services that are not authored by Valve, Valve does not screen such third-party content available on Steam or through other sources. Valve assumes no responsibility or liability for such third party content, unless to the extent provided by mandatory law. Some third-party application software is capable of being used by businesses for business purposes - however, you may only acquire such software via Steam for private personal use.</p>
	
	<a name="6"></a>
	<p>6. USER GENERATED CONTENT<a href="#0" style="text-decoration: none;"><small style="color: #666;">  ⏶</small></a></p>
			<p>A. General Provisions </p>
				<p>Steam provides interfaces and tools for you to be able to generate content and make it available to other users and/or to Valve at your sole discretion. "User Generated Content" means any content you make available to other users through your use of multi-user features of Steam, or to Valve or its affiliates through your use of the Content and Services or otherwise.</p>
				<p>When you upload your content to Steam to make it available to other users and/or to Valve, you grant Valve and its affiliates the worldwide, non-exclusive right to use, reproduce, modify, create derivative works from, distribute, transmit, transcode, translate, broadcast, and otherwise communicate, and publicly display and publicly perform, your User Generated Content, and derivative works of your User Generated Content, for the purpose of the operation, distribution, incorporation as part of and promotion of the Steam service, Steam games or other Steam offerings, including Subscriptions. This license is granted to Valve as the content is uploaded on Steam for the entire duration of the intellectual property rights. It may be terminated if Valve is in breach of the license and has not cured such breach within fourteen (14) days from receiving notice from you sent to the attention of the Valve Legal Department at the applicable Valve address noted on this <a target="new" style="text-decoration:underline;" href="http://store.steampowered.com/privacy_agreement/">Privacy Policy</a> page. The termination of said license does not affect the rights of any sub-licensees pursuant to any sub-license granted by Valve prior to termination of the license. Valve is the sole owner of the derivative works created by Valve from your User Generated Content, and is therefore entitled to grant licenses on these derivative works.  If you use Valve cloud storage, you grant us a license to store your information as part of that service.  Valve may place limits on the amount of storage you may use.</p>
				<p>If you provide Valve with any feedback or suggestions about Steam, the Content and Services, or any Valve products, Hardware or services, Valve is free to use the feedback or suggestions however it chooses, without any obligation to account to you.</p>
				<p>You agree that the User Generated Content you upload on Steam through the interfaces and tools provided by Valve is given significant exposure and that you share it for your enjoyment and for the recognition you may receive from other Subscribers. Consequently, you grant this license to Valve and its affiliates for free, notwithstanding any other contrary terms provided in App-Specific Terms, as defined under Section 6.B below.</p>
			<p>B. Content Uploaded to the Steam Workshop</p>
				<p>Some games or applications available on Steam ("Workshop-Enabled Apps") allow you to create User Generated Content based on or using the Workshop-Enabled App, and to submit that User Generated Content (a “Workshop Contribution”) to one or more Steam Workshop web pages.  Workshop Contributions can be viewed by the Steam community,  and for some categories of Workshop Contributions users may be able to interact with, download or purchase the Workshop Contribution.  In some cases, Workshop Contributions may be considered for incorporation by Valve or a third-party developer into a game or into a Subscription Marketplace.</p>  
				<p>You understand and agree that Valve is not obligated to use, distribute, or continue to distribute copies of any Workshop Contribution and reserves the right, but not the obligation, to restrict or remove Workshop Contributions for any reason.</p>
				<p>Specific Workshop-Enabled Apps or Workshop web pages may contain special terms (“App-Specific Terms”) that supplement or change the terms set out in this Section to reflect the individual requirements of the Workshop-Enabled App in question.</p>
				<p>Under Section 6.A, Workshop Contributions are in principle made available to Subscribers for free. By way of exception, they may be made available to Subscribers for a fee. In that case, the way the revenues generated may be shared, and in particular, the compensation you may receive as a result of this making available, are defined in the App-Specific Terms and not by this Agreement. Unless otherwise specified in App-Specific Terms (if any), the following general rules apply to Workshop Contributions.
		</p><p>
			</p><ul>
				<li>Workshop Contributions are Subscriptions, and therefore you agree that any Subscriber receiving distribution of your Workshop Contribution will have the same rights to use your Workshop Contribution (and will be subject to the same restrictions) as are set out in this Agreement for any other Subscriptions.<br>
				</li><li>Notwithstanding the license described in Section 6.A, Valve will only have the right to modify including to create derivative works from your Workshop Contribution in the following cases:  (a) Valve may make modifications necessary to make your Contribution compatible with Steam and the Workshop functionality or user interface, and (b) Valve or the applicable developer may make modifications to Workshop Contributions that are accepted for in-Application distribution as it deems necessary or desirable to enhance gameplay or make it compatible with the Workshop-Enabled App. Under Section 6.A, you grant for free to Valve and its affiliates the right to modify, including to create derivative works from, your Workshop Contribution. As a result, you are not entitled to any compensation from Valve as a result of Valve’s modifications.
				</li><li>You may, in your sole discretion, choose to remove a Workshop Contribution from the applicable Workshop pages.  If you do so, Valve will no longer have the right to use, distribute, transmit, communicate, publicly display or publicly perform the Workshop Contribution, except that (a) Valve may continue to exercise these rights for any Workshop Contribution that is accepted for distribution in-game or distributed in a manner that allows it to be used in-game, and (b) your removal will not affect the rights of any Subscriber who has already obtained access to a copy of the Workshop Contribution.
			</li></ul>
		<p></p>			
			<p>C. Promotions and Endorsements</p>
			<p>If you use Steam services (e.g. the Steam Curators’ Lists or the Steam Broadcasting service) to promote or endorse a product, service or event in return for any kind of consideration from a third party (including non-monetary rewards such as free games), you must clearly indicate the source of such consideration to your audience.</p>
			<p>D. Representations and Warranties</p>
				<p>You represent and warrant to us that you have sufficient rights in all User Generated Content to grant Valve and other affected parties the licenses described under A. and B. above or in any license terms specific to the applicable Workshop-Enabled App or Workshop page. This includes, without limitation, any kind of intellectual property rights or other proprietary or personal rights affected by or included in the User Generated Content.  In particular, with respect to Workshop Contributions, you represent and warrant that the Workshop Contribution was originally created by you (or, with respect to a Workshop Contribution to which others contributed besides you, by you and the other contributors, and in such case that you have the right to submit such Workshop Contribution on behalf of those other contributors). </p>
				<p>You furthermore represent and warrant that the User Generated Content, your submission of that Content, and your granting of rights in that Content does not violate any applicable contract, law or regulation.</p> 
	
	<a name="7"></a>
	<p>7. DISCLAIMERS; LIMITATION OF LIABILITY; NO GUARANTEES; LIMITED WARRANTY &amp; AGREEMENT<a href="#0" style="text-decoration: none;"><small style="color: #666;">  ⏶</small></a></p>
		<p>THIS SECTION 7 DOES NOT APPLY TO EU OR UK SUBSCRIBERS.</p>
		<p>
			</p><ul>
				<li>FOR AUSTRALIAN SUBSCRIBERS, THIS SECTION 7 DOES NOT EXCLUDE, RESTRICT OR MODIFY THE APPLICATION OF ANY GUARANTEE, RIGHT OR REMEDY THAT CANNOT BE SO EXCLUDED, RESTRICTED OR MODIFIED, INCLUDING THOSE CONFERRED BY THE AUSTRALIAN CONSUMER LAW (ACL). UNDER THE ACL, GOODS COME WITH GUARANTEES INCLUDING A GUARANTEE THAT GOODS ARE OF ACCEPTABLE QUALITY. IF THERE IS A FAILURE OF THIS GUARANTEE, YOU ARE ENTITLED TO A REMEDY (WHICH MAY INCLUDE HAVING THE GOODS REPAIRED OR REPLACED OR A REFUND). IF A REPAIR OR REPLACEMENT CANNOT BE PROVIDED OR THERE IS A MAJOR FAILURE, YOU ARE ENTITLED TO A REFUND.</li>
				<li>FOR NEW ZEALAND SUBSCRIBERS, THIS SECTION 7 DOES NOT EXCLUDE, RESTRICT OR MODIFY THE APPLICATION OF ANY RIGHT OR REMEDY THAT CANNOT BE SO EXCLUDED, RESTRICTED OR MODIFIED INCLUDING THOSE CONFERRED BY THE NEW ZEALAND CONSUMER GUARANTEES ACT 1993. UNDER THIS ACT ARE GUARANTEES WHICH INCLUDE THAT GOODS AND SERVICES ARE OF ACCEPTABLE QUALITY. IF THIS GUARANTEE IS NOT MET THERE ARE ENTITLEMENTS TO HAVE THE SOFTWARE REMEDIED (WHICH MAY INCLUDE REPAIR, REPLACEMENT OR REFUND). IF A REMEDY CANNOT BE PROVIDED OR THE FAILURE IS OF A SUBSTANTIAL CHARACTER, THE ACT PROVIDES FOR A REFUND.</li>
			</ul>
		<p></p>
		<p>Prior to acquiring a Subscription, you should consult the product information made available on Steam, including Subscription description, minimum technical requirements, and user reviews.</p>
			<p>A. DISCLAIMERS</p>
				<p>TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, VALVE AND ITS AFFILIATES AND SERVICE PROVIDERS EXPRESSLY DISCLAIM (I) ANY WARRANTY FOR STEAM, THE CONTENT AND SERVICES, AND THE SUBSCRIPTIONS, AND (II) ANY COMMON LAW DUTIES WITH REGARD TO STEAM, THE CONTENT AND SERVICES, AND THE SUBSCRIPTIONS, INCLUDING DUTIES OF LACK OF NEGLIGENCE AND LACK OF WORKMANLIKE EFFORT. STEAM, THE CONTENT AND SERVICES, THE SUBSCRIPTIONS, AND ANY INFORMATION AVAILABLE IN CONNECTION THEREWITH ARE PROVIDED ON AN "AS IS" AND "AS AVAILABLE" BASIS, "WITH ALL FAULTS" AND WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NONINFRINGEMENT. ANY WARRANTY AGAINST INFRINGEMENT THAT MAY BE PROVIDED IN SECTION 2-312 OF THE UNITED STATES UNIFORM COMMERCIAL CODE AND/OR IN ANY OTHER COMPARABLE STATE STATUTE IS EXPRESSLY DISCLAIMED. ALSO, THERE IS NO WARRANTY OF TITLE, NON-INTERFERENCE WITH YOUR ENJOYMENT, OR AUTHORITY IN CONNECTION WITH STEAM, THE CONTENT AND SERVICES, THE SUBSCRIPTIONS, OR INFORMATION AVAILABLE IN CONNECTION THEREWITH.</p>
				<p>ANY WARRANTY AGAINST INFRINGEMENT THAT MAY BE PROVIDED IN SECTION 2-312 OF THE UNITED STATES UNIFORM COMMERCIAL CODE IS EXPRESSLY DISCLAIMED.</p>
			<p>B. LIMITATION OF LIABILITY</p>
				<p>TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, NEITHER VALVE, ITS LICENSORS, NOR THEIR AFFILIATES, NOR ANY OF VALVE’S SERVICE PROVIDERS, SHALL BE LIABLE IN ANY WAY FOR LOSS OR DAMAGE OF ANY KIND RESULTING FROM THE USE OR INABILITY TO USE STEAM, YOUR ACCOUNT, YOUR SUBSCRIPTIONS AND THE CONTENT AND SERVICES INCLUDING, BUT NOT LIMITED TO, LOSS OF GOODWILL, WORK STOPPAGE, COMPUTER FAILURE OR MALFUNCTION, OR ANY AND ALL OTHER COMMERCIAL DAMAGES OR LOSSES. IN NO EVENT WILL VALVE BE LIABLE FOR ANY INDIRECT, INCIDENTAL, CONSEQUENTIAL, SPECIAL, PUNITIVE OR EXEMPLARY DAMAGES, OR ANY OTHER DAMAGES ARISING OUT OF OR IN ANY WAY CONNECTED WITH STEAM, THE CONTENT AND SERVICES, THE SUBSCRIPTIONS, AND ANY INFORMATION AVAILABLE IN CONNECTION THEREWITH, OR THE DELAY OR INABILITY TO USE THE CONTENT AND SERVICES, SUBSCRIPTIONS OR ANY INFORMATION, EVEN IN THE EVENT OF VALVE’S OR ITS AFFILIATES’ FAULT, TORT (INCLUDING NEGLIGENCE), STRICT LIABILITY, OR BREACH OF VALVE’S WARRANTY AND EVEN IF IT HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. THESE LIMITATIONS AND LIABILITY EXCLUSIONS APPLY EVEN IF ANY REMEDY FAILS TO PROVIDE ADEQUATE RECOMPENSE. </p>
				<p>BECAUSE SOME STATES OR JURISDICTIONS DO NOT ALLOW THE EXCLUSION OR THE LIMITATION OF LIABILITY FOR CONSEQUENTIAL OR INCIDENTAL DAMAGES, IN SUCH STATES OR JURISDICTIONS, EACH OF VALVE, ITS LICENSORS, AND ITS AFFILIATES’ LIABILITY SHALL BE LIMITED TO THE FULL EXTENT PERMITTED BY LAW.</p>
			<p>C. NO GUARANTEES</p>
				<p>TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, NEITHER VALVE NOR ITS AFFILIATES GUARANTEE CONTINUOUS, ERROR-FREE, VIRUS-FREE OR SECURE OPERATION AND ACCESS TO STEAM, THE CONTENT AND SERVICES, YOUR ACCOUNT AND/OR YOUR SUBSCRIPTION(S) OR ANY INFORMATION AVAILABLE IN CONNECTION THEREWITH.</p>
			<p>D. LIMITED WARRANTY &amp; AGREEMENT</p>
				<p>CERTAIN HARDWARE PURCHASED FROM VALVE IS SUBJECT TO A LIMITED WARRANTY &amp; AGREEMENT, [OR DEPENDING ON YOUR LOCATION, A STATUTORY WARRANTY] WHICH IS DESCRIBED IN DETAIL <a style="text-decoration:underline;" href="https://support.steampowered.com/kb_article.php?ref=4577-TUJV-6223">HERE</a>.</p>
	
	<a name="8"></a>
	<p>8. AMENDMENTS TO THIS AGREEMENT<a href="#0" style="text-decoration: none;"><small style="color: #666;">  ⏶</small></a></p>
		<p>PLEASE NOTE: If you are a consumer with place of residence in Germany, a different version of Section 8 applies to you, which is available <a style="text-decoration:underline;" href="http://store.steampowered.com/subscriber_agreement_de/">here</a>.</p>
			<p>A. Mutual Amendment</p>
				<p>This Agreement may at any time be mutually amended by your explicit consent to changes proposed by Valve.</p>
			<p>B. Unilateral Amendment</p>
				<p>Furthermore, Valve may amend this Agreement (including any Subscription Terms or Rules of Use) unilaterally at any time in its sole discretion. In this case, you will be notified by e-mail of any amendment to this Agreement made by Valve at least 30 (30) days before the effective date of the amendment. You can view the Agreement at any time at <a target="_new" href="http://www.steampowered.com/">http://www.steampowered.com/</a>. Your failure to cancel your Account prior to the effective date of the amendment will constitute your acceptance of the amended terms. If you don’t agree to the amendments or to any of the terms in this Agreement, your only remedy is to cancel your Account or to cease use of the affected Subscription(s). Valve shall not have any obligation to refund any fees that may have accrued to your Account before cancellation of your Account or cessation of use of any Subscription, nor shall Valve have any obligation to prorate any fees in such circumstances.</p>
	
	<a name="9"></a>
	<p>9. TERM AND TERMINATION<a href="#0" style="text-decoration: none;"><small style="color: #666;">  ⏶</small></a></p>
			<p>A. Term</p>
				<p>The term of this Agreement (the "Term") commences on the date you first indicate your acceptance of these terms, and will continue in effect until otherwise terminated in accordance with this Agreement.</p>
			<p>B. Termination by You</p>
				<p>You may cancel your Account at any time.  You may cease use of a Subscription at any time or, if you choose, you may request that Valve terminate your access to a Subscription.  However, Subscriptions are not transferable, and even if your access to a Subscription for a particular game or application is terminated, the original activation key will not be able to be registered to any other account, even if the Subscription was obtained in a retail store.  Access to Subscriptions ordered as a part of a pack or bundle cannot be terminated individually, termination of access to one game within the bundle will result in termination of access to all games ordered in the pack.  Your cancellation of an Account, or your cessation of use of any Subscription or request that access to a Subscription be terminated, will not entitle you to any refund, including of any Subscription fees.  Valve reserves the right to collect fees, surcharges or costs incurred prior to the cancellation of your Account or termination of your access to a particular Subscription. In addition, you are responsible for any charges incurred to third-party vendors or content providers before your cancellation. </p>
			<p>C. Termination by Valve</p>
				<p>Valve may restrict or cancel your Account or any particular Subscription(s) at any time in the event that (a) Valve ceases providing such Subscriptions to similarly situated Subscribers generally, or (b) you breach any terms of this Agreement (including any Subscription Terms or Rules of Use). In the event that your Account or a particular Subscription is restricted or terminated or cancelled by Valve for a violation of this Agreement or improper or illegal activity, no refund, including of any Subscription fees or of any unused funds in your Steam Wallet, will be granted.</p>
			<p>D. Survival of Terms</p>
				<p>Sections 2.C., 2.D., 2.F., 2.G., 3.A., 3.B., 3.D., 3.H., and 5 - 11 will survive any expiration or termination of this Agreement.</p>
	
	<a name="10"></a>
	<p>10. APPLICABLE LAW/JURISDICTION<a href="#0" style="text-decoration: none;"><small style="color: #666;">  ⏶</small></a></p>
		<p>Most user concerns can be resolved by use of our Steam support site at <a target="_new" href="https://support.steampowered.com/">https://support.steampowered.com/</a>. If Valve is unable to resolve your concerns and a dispute remains between you and Valve, this Section explains how the parties have agreed to resolve it.</p>
		<p>For All Subscribers Outside the European Union and United Kingdom:</p>
		<p>You and Valve agree that this Agreement shall be deemed to have been made and executed in the State of Washington, U.S.A., and Washington law, excluding conflict of laws principles and the Convention on Contracts for the International Sale of Goods, governs all disputes and claims arising out of or relating to: (i) any aspect of the relationship between us; (ii) this Agreement; or (iii) your use of Steam, your Account or the Content and Services. You and Valve agree that all disputes and claims between you and Valve (including any dispute or claim that arose before the existence of this or any prior agreement) shall be commenced and maintained exclusively in any state or federal court located in King County, Washington, having subject matter jurisdiction. You and Valve hereby consent to the exclusive jurisdiction of such courts and waive any objections as to personal jurisdiction or venue in such courts. </p>
		<p>If the laws where you live mandate alternative dispute resolution options, you may seek a remedy under those options.  If you are a consumer who lives in Russia, you may also seek a remedy with local Russian state courts.</p>
		<p>For EU and UK Subscribers:</p>
		<p>This Agreement is governed by the law of the country where you have your habitual residence.</p>
		<p>In the event of a dispute relating to the interpretation, the performance or the validity of the Subscriber Agreement, an amicable solution may be sought before any legal action. You can file your complaint at <a style="text-decoration:underline;" href="http://help.steampowered.com">http://help.steampowered.com</a>. 
		
	<a name="11"></a>
	</p><p>11. MISCELLANEOUS<a href="#0" style="text-decoration: none;"><small style="color: #666;">  ⏶</small></a></p>
		<p>In the event that any provision of this Agreement is held by a court to be invalid or unenforceable, such provision will be deemed severable and the remaining provisions of this Agreement shall remain in full force and effect.</p>
		<p>This Agreement, including any Subscription Terms, Rules of Use, the Valve Privacy Policy, and the Valve Hardware Limited Warranty Policy, constitutes and contains the entire agreement between the parties with respect to the subject matter hereof and supersedes any prior oral or written agreements. You agree that this Agreement is not intended to confer and does not confer any rights or remedies upon any person other than the parties to this Agreement.</p>
		<p>Valve’s obligations are subject to existing laws and legal process and Valve may comply with law enforcement or regulatory requests or requirements notwithstanding any contrary term.</p>
		<p>You agree to comply with all applicable import/export laws and regulations. You agree not to export the Content and Services or Hardware or allow use of your Account by individuals of any terrorist supporting countries to which encryption exports are at the time of exportation restricted by the U.S. Bureau of Export Administration. You represent and warrant that you are not located in, under the control of, or a national or resident of any such prohibited country.</p>
		<p>This Agreement was last updated on September 18, 2025 ("Revision Date"). If you were a Subscriber before the Revision Date, it replaces and supersedes your existing agreement with Valve or Valve SARL on the day that it becomes effective according to Section 8 above.</p>
</div>		</div>

		
					<div style="clear: both;"></div>
			<a href="https://store.steampowered.com/ssa_feedback/" target="_blank" rel="">Privacy Feedback</a>
			</div>
</div>


		</div>	<!-- responsive_page_legacy_content -->

		<div id="footer_spacer" style="" class=""></div>
<div id="footer" role="contentinfo" class="">
<div class="footer_content">

    <div class="rule"></div>
				<div id="footer_logo_steam"><img src="https://store.akamai.steamstatic.com/public/images/v6/logo_steam_footer.png" alt="Valve Software" border="0"></div>

    <div id="footer_logo"><a href="http://www.valvesoftware.com" target="_blank" rel=""><img src="https://store.akamai.steamstatic.com/public/images/footerLogo_valve_new.png" alt="Valve Software" border="0"></a></div>
    <div id="footer_text" data-panel="{&quot;flow-children&quot;:&quot;row&quot;}">
        <div>© 2025 Valve Corporation.  All rights reserved.  All trademarks are property of their respective owners in the US and other countries.</div>
        <div>VAT included in all prices where applicable.&nbsp;&nbsp;

            <a href="https://store.steampowered.com/privacy_agreement/?snr=1_44_44_" target="_blank" rel="">Privacy Policy</a>
            &nbsp; <span aria-hidden="true">|</span> &nbsp;
            <a href="https://store.steampowered.com/legal/?snr=1_44_44_" target="_blank" rel="">Legal</a>
            &nbsp; <span aria-hidden="true">|</span> &nbsp;
            <a href="https://help.steampowered.com/faqs/view/10BB-D27A-6378-4436?snr=1_44_44_" target="_blank" rel="">Accessibility</a>
            &nbsp; <span aria-hidden="true">|</span> &nbsp;
            <a href="https://store.steampowered.com/subscriber_agreement/?snr=1_44_44_" target="_blank" rel="">Steam Subscriber Agreement</a>
            &nbsp; <span aria-hidden="true">|</span> &nbsp;
            <a href="https://store.steampowered.com/steam_refunds/?snr=1_44_44_" target="_blank" rel="">Refunds</a>
            &nbsp; <span aria-hidden="true">|</span> &nbsp;
            <a href="https://store.steampowered.com/account/cookiepreferences/?snr=1_44_44_" target="_blank" rel="">Cookies</a>

        </div>
					<div class="responsive_optin_link">
				<div class="btn_medium btnv6_grey_black" role="link" onclick="Responsive_RequestMobileView()">
					<span>View mobile website</span>
				</div>
			</div>
		
    </div>



    <div style="clear: left;"></div>
	<br>

    <div class="rule"></div>

    <div class="valve_links" data-panel="{&quot;flow-children&quot;:&quot;row&quot;}">
        <a href="http://www.valvesoftware.com/about" target="_blank" rel="">About Valve</a>
        &nbsp; <span aria-hidden="true">|</span> &nbsp;<a href="http://www.valvesoftware.com" target="_blank" rel="">Jobs</a>
        &nbsp; <span aria-hidden="true">|</span> &nbsp;<a href="http://www.steampowered.com/steamworks/" target="_blank" rel="">Steamworks</a>
        &nbsp; <span aria-hidden="true">|</span> &nbsp;<a href="https://partner.steamgames.com/steamdirect" target="_blank" rel="">Steam Distribution</a>
        &nbsp; <span aria-hidden="true">|</span> &nbsp;<a href="https://help.steampowered.com/en/?snr=1_44_44_">Support</a>
                        		&nbsp; <span aria-hidden="true">|</span> &nbsp;<a href="https://store.steampowered.com/digitalgiftcards/?snr=1_44_44_" target="_blank" rel="">Gift Cards</a>
		&nbsp; <span aria-hidden="true">|</span> &nbsp;<a href="https://steamcommunity.com/linkfilter/?u=http%3A%2F%2Fwww.facebook.com%2FSteam" target="_blank" rel=" noopener"><img src="https://store.akamai.steamstatic.com/public/images/ico/ico_facebook.png" alt="Facebook: Steam"></a>
		&nbsp; <span aria-hidden="true">|</span> &nbsp;<a href="http://twitter.com/steam" target="_blank" rel=""><img src="https://store.akamai.steamstatic.com/public/images/ico/ico_twitter.png" alt="X: @Steam"></a>
			&nbsp; <span aria-hidden="true">|</span> &nbsp;<a href="https://steamcommunity.com/linkfilter/?u=https%3A%2F%2Fbsky.app%2Fprofile%2Fsteampowered.com" target="_blank" rel=" noopener"><img src="https://store.akamai.steamstatic.com/public/images/ico/ico_bsky.png" alt="Bluesky: Steampowered"></a>
            </div>
				<div class="extra_space"></div>
	
</div>
</div>

	</div>	<!-- responsive_page_content -->

</div><div class="miniprofile_hover" style="display: none;"><div class="shadow_ul"></div><div class="shadow_top"></div><div class="shadow_ur"></div><div class="shadow_left"></div><div class="shadow_right"></div><div class="shadow_bl"></div><div class="shadow_bottom"></div><div class="shadow_br"></div><div class="miniprofile_hover_inner shadow_content"></div></div>	<!-- responsive_page_frame -->

<div class="FullModalOverlay" style="display: none;"><div class="ModalOverlayContent ModalOverlayBackground"></div></div></body></html>
""".strip()


def main() -> None:
    # 1) trafilatura 전처리
    trafilatura_result = extract(HTML_SOURCE, output_format="html")
    if not trafilatura_result:
        print("trafilatura 전처리 결과가 비어 있습니다.")
        return

    # 2) _normalize_block 전처리
    normalized_result = _normalize_block(trafilatura_result)

    # 결과 출력
    print("\n=== _normalize_block 결과 ===")
    print(normalized_result)


if __name__ == "__main__":
    main()
