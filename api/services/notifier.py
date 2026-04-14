import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

async def enviar_correo(asunto: str, cuerpo: str, destinatario: str = None):
    dest = destinatario or os.getenv("SMTP_DEST")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"[DocuMind] {asunto}"
    msg["From"] = os.getenv("SMTP_USER")
    msg["To"] = dest

    html = f"""
    <html><body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
      <div style="background: #1D9E75; padding: 20px; border-radius: 8px 8px 0 0;">
        <h1 style="color: white; margin: 0; font-size: 22px;">DocuMind</h1>
        <p style="color: #9FE1CB; margin: 4px 0 0; font-size: 13px;">Sistema de gestión documental inteligente</p>
      </div>
      <div style="border: 1px solid #e0e0e0; border-top: none; padding: 24px; border-radius: 0 0 8px 8px;">
        {cuerpo}
      </div>
      <p style="font-size: 11px; color: #aaa; text-align: center; margin-top: 12px;">
        Self-hosted · Datos privados · github.com/sergionet17/documind
      </p>
    </body></html>
    """

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as server:
        server.starttls()
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
        server.sendmail(os.getenv("SMTP_USER"), dest, msg.as_string())

    return {"enviado": True, "destinatario": dest}


async def enviar_sugerencia_correo(sugerencia: dict):
    cuerpo = f"""
    <h2 style="color: #1D9E75;">Nueva sugerencia detectada</h2>
    <table style="width:100%; font-size: 14px; border-collapse: collapse;">
      <tr><td style="color:#666; padding: 6px 0; width:120px;">Categoría</td>
          <td><span style="background:#E1F5EE; color:#085041; padding:2px 8px; border-radius:4px;">{sugerencia.get('categoria','')}</span></td></tr>
      <tr><td style="color:#666; padding: 6px 0;">Fuente</td>
          <td>{sugerencia.get('fuente','')}</td></tr>
      <tr><td style="color:#666; padding: 6px 0;">Título</td>
          <td><strong>{sugerencia.get('titulo','')}</strong></td></tr>
    </table>
    <div style="background:#f9f9f9; border-left: 3px solid #1D9E75; padding: 12px; margin: 16px 0; font-size: 14px; line-height: 1.6;">
      {sugerencia.get('texto','')}
    </div>
    {"<a href='" + sugerencia['url'] + "' style='color:#1D9E75;'>Ver fuente original</a>" if sugerencia.get('url') else ''}
    """
    return await enviar_correo(f"Sugerencia: {sugerencia.get('titulo','')}", cuerpo)


async def enviar_resumen_diario(sugerencias: list):
    if not sugerencias:
        return {"enviado": False, "razon": "sin sugerencias"}

    items = ""
    for s in sugerencias:
        items += f"""
        <tr>
          <td style="padding:8px; border-bottom:1px solid #eee;">
            <span style="background:#E1F5EE;color:#085041;padding:2px 6px;border-radius:4px;font-size:12px;">{s.get('categoria','')}</span>
          </td>
          <td style="padding:8px; border-bottom:1px solid #eee; font-size:14px;">{s.get('titulo','')}</td>
        </tr>"""

    cuerpo = f"""
    <h2 style="color:#1D9E75;">Resumen diario — {len(sugerencias)} sugerencias</h2>
    <table style="width:100%; border-collapse:collapse;">
      <tr style="background:#f5f5f5;">
        <th style="padding:8px; text-align:left; font-size:13px; color:#666;">Categoría</th>
        <th style="padding:8px; text-align:left; font-size:13px; color:#666;">Título</th>
      </tr>
      {items}
    </table>
    <p style="margin-top:16px; font-size:13px; color:#666;">
      Accede al dashboard para ver el detalle completo de cada sugerencia.
    </p>
    """
    return await enviar_correo(f"Resumen diario — {len(sugerencias)} sugerencias nuevas", cuerpo)
