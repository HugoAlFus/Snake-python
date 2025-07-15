def overlay_image(background, overlay, x, y):
    h, w = overlay.shape[:2]

    if x < 0 or y < 0 or x + w > background.shape[1] or y + h > background.shape[0]:
        return  # fuera del frame

    overlay_rgb = overlay[:, :, :3]
    mask = overlay[:, :, 3:] / 255.0
    inv_mask = 1.0 - mask

    roi = background[y:y + h, x:x + w]

    for c in range(3):
        roi[:, :, c] = roi[:, :, c] * inv_mask[:, :, 0] + overlay_rgb[:, :, c] * mask[:, :, 0]

    background[y:y + h, x:x + w] = roi