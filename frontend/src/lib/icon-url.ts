// As skills guardam o ícone como classe devicon (ex: "devicon-python-plain")
// desde a Etapa 5 — mantemos essa string como id estável (dado salvo no
// banco/estático), mas renderizamos com o SVG individual do devicon em vez
// da webfont completa (~1.4MB pra mostrar 10 ícones). Ver public/icons/devicon/.
export function devIconSvg(iconClass: string): string {
  return `/icons/devicon/${iconClass.replace(/^devicon-/, "")}.svg`;
}
