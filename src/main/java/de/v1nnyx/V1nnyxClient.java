package de.v1nnyx;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.message.v1.ClientReceiveMessageEvents;
import net.minecraft.client.Minecraft;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.contents.TranslatableContents;
import net.minecraft.resources.Identifier;
import net.minecraft.sounds.SoundEvent;

/**
 * V1NNYX Mod - rein clientseitig, funktioniert auf jedem Server.
 *
 * Erkennt an der Todesnachricht des Servers ("death.attack.player" usw.),
 * dass DU einen anderen SPIELER getoetet hast, und spielt dann zufaellig
 * einen der Songs aus dem Soundevent "v1nnyx:kill_song".
 *
 * Hinweis: In aelteren Versionen (vor 1.21.11) heisst die Klasse
 * net.minecraft.resources.Identifier noch ResourceLocation.
 */
public class V1nnyxClient implements ClientModInitializer {

    public static final String MOD_ID = "v1nnyx";

    private static final SoundEvent KILL_SONG = SoundEvent.createVariableRangeEvent(
            Identifier.fromNamespaceAndPath(MOD_ID, "kill_song"));

    private static long lastPlayed = 0L;

    @Override
    public void onInitializeClient() {
        ClientReceiveMessageEvents.GAME.register((message, overlay) -> {
            if (overlay) {
                return;
            }
            Minecraft mc = Minecraft.getInstance();
            if (mc.player == null || mc.getConnection() == null) {
                return;
            }
            if (isMyPlayerKill(mc, message)) {
                mc.execute(() -> playKillSong(mc));
            }
        });
    }

    /** True, wenn die Nachricht eine Todesnachricht ist, in der ich der Killer und das Opfer ein Spieler ist. */
    private static boolean isMyPlayerKill(Minecraft mc, Component message) {
        if (!(message.getContents() instanceof TranslatableContents tc)) {
            return false;
        }
        if (!tc.getKey().startsWith("death.")) {
            return false;
        }
        Object[] args = tc.getArgs();
        if (args.length < 2) {
            return false;
        }

        String victim = argToString(args[0]);
        String killer = argToString(args[1]);
        String me = mc.player.getName().getString();

        if (!killer.equals(me) || victim.equals(me)) {
            return false;
        }
        // Opfer muss ein Spieler sein (steht in der Tab-Liste), keine Mob-Entitaet.
        return mc.getConnection().getPlayerInfo(victim) != null;
    }

    private static String argToString(Object arg) {
        if (arg instanceof Component c) {
            return c.getString();
        }
        return String.valueOf(arg);
    }

    private static void playKillSong(Minecraft mc) {
        long now = System.currentTimeMillis();
        if (now - lastPlayed < 1500L) {
            return; // Doppel-Ausloesung verhindern
        }
        lastPlayed = now;
        mc.getSoundManager().play(SimpleSoundInstance.forUI(KILL_SONG, 1.0F, 1.0F));
    }
}
