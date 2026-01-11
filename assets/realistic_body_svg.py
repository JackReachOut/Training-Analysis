# realistic_body_svg.py
# Contains SVG markup and CSS for the realistic human body visualization

REALISTIC_BODY_SVG = '''
<!-- Human Body //-->
<div class="human-body">
    <svg data-position='head' id='head' class='head' xmlns='http://www.w3.org/2000/svg' width='56.594' height='95.031' viewBox='0 0 56.594 95.031'><path d='M15.92 68.5l8.8 12.546 3.97 13.984-9.254-7.38-4.622-15.848zm27.1 0l-8.8 12.546-3.976 13.988 9.254-7.38 4.622-15.848zm6.11-27.775l.108-11.775-21.16-14.742L8.123 26.133 8.09 40.19l-3.24.215 1.462 9.732 5.208 1.81 2.36 11.63 9.72 11.018 10.856-.324 9.56-10.37 1.918-11.952 5.207-1.81 1.342-9.517zm-43.085-1.84l-.257-13.82L28.226 11.9l23.618 15.755-.216 10.37 4.976-17.085L42.556 2.376 25.49 0 10.803 3.673.002 24.415z'/></svg>
    <svg data-position='left-shoulder' id='left-shoulder' class='left-shoulder' xmlns='http://www.w3.org/2000/svg' width='109.532' height='46.594' viewBox='0 0 109.532 46.594'><path d='m 38.244,-0.004 1.98,9.232 -11.653,2.857 -7.474,-2.637 z M 17.005,10.536 12.962,8.35 0.306,22.35 0.244,27.675 c 0,0 16.52,-17.015 16.764,-17.14 z m 1.285,0.58 C 18.3,11.396 0.528,30.038 0.528,30.038 L -0.01,46.595 6.147,36.045 18.017,30.989 26.374,15.6 Z'/></svg>
    <svg data-position='right-shoulder' id='right-shoulder' class='right-shoulder' xmlns='http://www.w3.org/2000/svg' width='109.532' height='46.594' viewBox='0 0 109.532 46.594'><path d='m 3.2759972,-0.004 -1.98,9.232 11.6529998,2.857 7.473999,-2.637 z m 21.2379988,10.54 4.044,-2.187 12.656,14 0.07,5.33 c 0,0 -16.524,-17.019 -16.769,-17.144 z m -1.285,0.58 c -0.008,0.28 17.762,18.922 17.762,18.922 l 0.537,16.557 -6.157,-10.55 -11.871,-5.057 L 15.147997,15.6 Z'/></svg>
    <svg data-position='left-arm' id='left-arm' class='left-arm' xmlns='http://www.w3.org/2000/svg' width='156.344' height='119.25' viewBox='0 0 156.344 119.25'><path d='m21.12,56.5a1.678,1.678 0 0 1 -0.427,0.33l0.935,8.224l12.977,-13.89l1.2,-8.958a168.2,168.2 0 0 0 -14.685,14.294zm1.387,12.522l-18.07,48.91l5.757,1.333l19.125,-39.44l3.518,-22.047l-10.33,11.244zm-5.278,-18.96l2.638,18.74l-17.2,46.023l-2.657,-1.775l6.644,-35.518l10.575,-27.47zm18.805,-12.323a1.78,1.78 0 0 1 0.407,-0.24l3.666,-27.345l-7.037,-10.139l-7.258,10.58l-6.16,37.04l0.566,4.973a151.447,151.447 0 0 1 15.808,-14.87l0.008,0.001zm-13.742,-28.906l-3.3,35.276l-2.2,-26.238l5.5,-9.038z'/></svg>
    <svg data-position='right-arm' id='right-arm' class='right-arm' xmlns='http://www.w3.org/2000/svg' width='156.344' height='119.25' viewBox='0 0 156.344 119.25'><path d='m 18.997,56.5 a 1.678,1.678 0 0 0 0.427,0.33 L 18.489,65.054 5.512,51.164 4.312,42.206 A 168.2,168.2 0 0 1 18.997,56.5 Z m -1.387,12.522 18.07,48.91 -5.757,1.333 L 10.798,79.825 7.28,57.778 17.61,69.022 Z m 5.278,-18.96 -2.638,18.74 17.2,46.023 2.657,-1.775 L 33.463,77.532 22.888,50.062 Z M 4.083,37.739 A 1.78,1.78 0 0 0 3.676,37.499 L 0.01,10.154 7.047,0.015 l 7.258,10.58 6.16,37.04 -0.566,4.973 A 151.447,151.447 0 0 0 4.091,37.738 l -0.008,10e-4 z m 13.742,-28.906 3.3,35.276 2.2,-26.238 -5.5,-9.038 z'/></svg>
    <svg data-position='chest' id='chest' class='chest' xmlns='http://www.w3.org/2000/svg' width='86.594' height='45.063' viewBox='0 0 86.594 45.063'><path d='M19.32 0l-9.225 16.488-10.1 5.056 6.15 4.836 4.832 14.07 11.2 4.616 17.85-8.828-4.452-34.7zm47.934 0l9.225 16.488 10.1 5.056-6.15 4.836-4.833 14.07-11.2 4.616-17.844-8.828 4.45-34.7z'/></svg>
    <svg data-position='stomach' id='stomach' class='stomach' xmlns='http://www.w3.org/2000/svg' width='75.25' height='107.594' viewBox='0 0 75.25 107.594'><path d='M19.25 7.49l16.6-7.5-.5 12.16-14.943 7.662zm-10.322 8.9l6.9 3.848-.8-9.116zm5.617-8.732L1.32 2.15 6.3 15.6zm-8.17 9.267l9.015 5.514 1.54 11.028-8.795-5.735zm15.53 5.89l.332 8.662 12.286-2.665.664-11.826zm14.61 84.783L33.28 76.062l-.08-20.53-11.654-5.736-1.32 37.5zM22.735 35.64L22.57 46.3l11.787 3.166.166-16.657zm-14.16-5.255L16.49 35.9l1.1 11.25-8.8-7.06zm8.79 22.74l-9.673-7.28-.84 9.78L-.006 68.29l10.564 14.594 5.5.883 1.98-20.735zM56 7.488l-16.6-7.5.5 12.16 14.942 7.66zm10.32 8.9l-6.9 3.847.8-9.116zm-5.617-8.733L73.93 2.148l-4.98 13.447zm8.17 9.267l-9.015 5.514-1.54 11.03 8.8-5.736zm-15.53 5.89l-.332 8.662-12.285-2.665-.664-11.827zm-14.61 84.783l3.234-31.536.082-20.532 11.65-5.735 1.32 37.5zm13.78-71.957l.166 10.66-11.786 3.168-.166-16.657zm14.16-5.256l-7.915 5.514-1.1 11.25 8.794-7.06zm-8.79 22.743l9.673-7.28.84 9.78 6.862 12.66-10.564 14.597-5.5.883-1.975-20.74z'/></svg>
    <!-- ...other SVGs for legs, hands, feet... -->
</div>
'''

REALISTIC_BODY_CSS = '''
/* Light neutral background for body parts for dark mode visibility */
.human-body {
    position: relative;
    width: 220px;
    height: 500px;
    margin: 0 auto;
    min-height: 400px;
}
.human-body svg {
    position: absolute;
    pointer-events: none;
}
/* Explicit positioning for each SVG part (tweak as needed for best fit) */
.head { left: 82px; top: 10px; z-index: 2; }
.left-shoulder { left: 20px; top: 70px; z-index: 2; }
.right-shoulder { left: 110px; top: 70px; z-index: 2; }
.chest { left: 60px; top: 110px; z-index: 2; }
.back { left: 55px; top: 120px; z-index: 1; opacity: 0.5; }
.stomach { left: 70px; top: 170px; z-index: 2; }
.left-arm { left: 0px; top: 120px; z-index: 2; }
.right-arm { left: 150px; top: 120px; z-index: 2; }
.left-leg { left: 50px; top: 270px; z-index: 2; }
.right-leg { left: 110px; top: 270px; z-index: 2; }
.left-hand { left: 0px; top: 220px; z-index: 2; }
.right-hand { left: 170px; top: 220px; z-index: 2; }
.left-foot { left: 60px; top: 420px; z-index: 2; }
.right-foot { left: 120px; top: 420px; z-index: 2; }
/* Highlighting classes to be added dynamically */
@media (prefers-color-scheme: dark) {
    .human-body svg path,
    .human-body svg rect,
    .human-body svg ellipse,
    .human-body svg polygon,
    .human-body svg circle {
        fill: #f5e6da !important; /* light for dark mode */
    }
}
@media (prefers-color-scheme: light) {
    .human-body svg path,
    .human-body svg rect,
    .human-body svg ellipse,
    .human-body svg polygon,
    .human-body svg circle {
        fill: #222 !important; /* dark for light mode */
    }
}
.highlight {
    filter: drop-shadow(0 0 8px #FF5722);
    opacity: 1.0;
}
'''


def render_realistic_body_html(highlighted=None):
    """
    Returns HTML for the realistic SVG human body, with highlighted muscle groups.
    highlighted: list of muscle class names to highlight (e.g., ['chest', 'left-arm'])
    """
    highlighted = highlighted or []
    # List of all possible body part classes
    body_parts = [
        'head', 'left-shoulder', 'right-shoulder', 'left-arm', 'right-arm',
        'chest', 'back', 'stomach', 'left-leg', 'right-leg',
        'left-hand', 'right-hand', 'left-foot', 'right-foot'
    ]
    # Add highlight class to selected parts in SVG markup
    html = REALISTIC_BODY_SVG
    for part in highlighted:
        if part in body_parts:
            # Add 'highlight' class to the SVG element
            html = html.replace(f'class="{part}"', f'class="{part} highlight"')
    # Add CSS
    html = f'<style>{REALISTIC_BODY_CSS}</style>' + html
    return html