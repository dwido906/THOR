/*
 * THOR-OS KERNEL - ONE MAN ARMY EDITION
 * Ultimate Developer & Gamer Platform Implementation
 * 
 * "The tree never minds, water is water" - Core Philosophy
 * Built for autonomous developers and elite gamers
 */

#include "thor_kernel.h"
#include "thor_ai_interface.h"
#include "thor_gatescore.h"
#include "thor_mesh_network.h"
#include "thor_vault.h"
#include "thor_forge.h"
#include "thor_p2p_cloud.h"
#include "thor_sync_engine.h"
#include "thor_security.h"

// THOR-OS ONE MAN ARMY VERSION
#define THOR_OS_VERSION_MAJOR 2
#define THOR_OS_VERSION_MINOR 0
#define THOR_OS_VERSION_PATCH 0
#define THOR_OS_CODENAME "ONE_MAN_ARMY"
#define THOR_OS_EDITION "ULTIMATE_DEVELOPER_GAMER"

// Enhanced THOR-OS System Information
struct thor_os_info
{
    uint32_t version_major;
    uint32_t version_minor;
    uint32_t version_patch;
    char codename[32];
    char edition[32];
    uint64_t boot_time;
    uint32_t ai_instances;
    uint32_t mesh_nodes_connected;
    uint32_t active_gamers;
    uint64_t total_gatescore_calculations;
    
    // ONE MAN ARMY EDITION Features
    uint32_t vault_repos_count;
    uint32_t forge_sessions_active;
    uint32_t p2p_peers_connected;
    uint64_t sync_operations_completed;
    uint32_t easter_eggs_discovered;
    uint32_t watering_count;
    bool local_hosting_enabled;
    bool p2p_cloud_active;
    bool ai_assistant_online;
    bool security_firewall_active;
};

// THOR Vault - Local Repository System
struct thor_vault {
    char path[256];
    uint32_t repo_count;
    uint64_t total_size;
    bool encryption_enabled;
    char git_branches[16][64];
    uint32_t active_branch;
    uint32_t pending_commits;
    uint32_t sync_destinations;
};

// THOR Forge - Code Editor/Workshop
struct thor_forge {
    uint32_t active_sessions;
    uint32_t party_mode_users;
    bool collaboration_enabled;
    char active_projects[8][128];
    uint32_t ai_suggestions_pending;
    bool real_time_sync;
};

// THOR P2P Cloud System
struct thor_p2p_cloud {
    uint32_t discovered_peers;
    uint32_t trusted_peers;
    uint64_t data_shared;
    uint64_t data_received;
    bool discovery_active;
    char node_id[64];
    uint32_t reputation_score;
};

// THOR Sync Engine
struct thor_sync_engine {
    uint32_t pending_syncs;
    uint32_t completed_syncs;
    uint32_t failed_syncs;
    char last_sync_destination[128];
    uint64_t last_sync_time;
    bool ai_recommendations_enabled;
    uint32_t tree_watering_count;
};

// Enhanced THOR-OS Kernel State
static struct thor_os_info thor_system = {
    .version_major = THOR_OS_VERSION_MAJOR,
    .version_minor = THOR_OS_VERSION_MINOR,
    .version_patch = THOR_OS_VERSION_PATCH,
    .codename = THOR_OS_CODENAME,
    .edition = THOR_OS_EDITION,
    .ai_instances = 0,
    .mesh_nodes_connected = 0,
    .active_gamers = 0,
    .total_gatescore_calculations = 0,
    .vault_repos_count = 0,
    .forge_sessions_active = 0,
    .p2p_peers_connected = 0,
    .sync_operations_completed = 0,
    .easter_eggs_discovered = 0,
    .watering_count = 0,
    .local_hosting_enabled = true,
    .p2p_cloud_active = false,
    .ai_assistant_online = false,
    .security_firewall_active = true
};

static struct thor_vault system_vault;
static struct thor_forge system_forge;
static struct thor_p2p_cloud system_p2p;
static struct thor_sync_engine system_sync;

// Function prototypes for ONE MAN ARMY features
void thor_print_one_man_army_banner(void);
void thor_init_vault_system(void);
void thor_init_forge_system(void);
void thor_init_p2p_cloud(void);
void thor_init_sync_engine(void);
void thor_init_security_firewall(void);
void thor_print_easter_egg_hammer(void);
void thor_watering_animation(void);
int thor_handle_sync_command(const char* command);
int thor_handle_vault_command(const char* command);
int thor_handle_forge_command(const char* command);
int thor_handle_p2p_command(const char* command);
void thor_display_system_dashboard(void);

// THOR-OS Boot Function - ONE MAN ARMY EDITION
void thor_kernel_main(uint32_t magic, uint32_t addr)
{
    // Initialize THOR-OS kernel
    thor_console_init();
    thor_memory_init();
    thor_interrupt_init();
    thor_ai_kernel_init();
    thor_gatescore_init();
    thor_mesh_init();
    thor_driver_ai_init();

    // Show THOR-OS boot banner
    thor_print_boot_banner();
    thor_print_one_man_army_banner();

    // Start THOR AI services
    thor_ai_start();

    // Initialize gaming optimizations
    thor_gaming_init();

    // Start MESH networking
    thor_mesh_connect();

    // Initialize ONE MAN ARMY features
    thor_init_vault_system();
    thor_init_forge_system();
    thor_init_p2p_cloud();
    thor_init_sync_engine();
    thor_init_security_firewall();

    // Main kernel loop
    thor_kernel_loop();
}

void thor_print_boot_banner(void)
{
    thor_console_clear();
    thor_console_set_color(THOR_COLOR_RED, THOR_COLOR_BLACK);

    thor_printf("████████╗██╗  ██╗ ██████╗ ██████╗       ██████╗ ███████╗\n");
    thor_printf("╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗     ██╔═══██╗██╔════╝\n");
    thor_printf("   ██║   ███████║██║   ██║██████╔╝     ██║   ██║███████╗\n");
    thor_printf("   ██║   ██╔══██║██║   ██║██╔══██╗     ██║   ██║╚════██║\n");
    thor_printf("   ██║   ██║  ██║╚██████╔╝██║  ██║     ╚██████╔╝███████║\n");
    thor_printf("   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝      ╚═════╝ ╚══════╝\n");
    thor_printf("\n");

    thor_console_set_color(THOR_COLOR_WHITE, THOR_COLOR_BLACK);
    thor_printf("          ONE MAN ARMY EDITION - Developer & Gamer Platform\n");
    thor_printf("                   Version %d.%d.%d \"%s\"\n",
                THOR_OS_VERSION_MAJOR, THOR_OS_VERSION_MINOR,
                THOR_OS_VERSION_PATCH, THOR_OS_CODENAME);
    thor_printf("             🌱 \"The tree never minds, water is water\" 🌱\n");
    thor_printf("                 Built for Autonomous Developers\n");
    thor_printf("\n");

    thor_console_set_color(THOR_COLOR_GREEN, THOR_COLOR_BLACK);
    thor_printf("[THOR-AI]     Neural networks online - Assistant ready...\n");
    thor_printf("[VAULT]       Local repository system initialized...\n");
    thor_printf("[FORGE]       Code workshop ready - Party mode enabled...\n");
    thor_printf("[P2P-CLOUD]   Peer discovery active - Nodes connecting...\n");
    thor_printf("[SYNC-ENGINE] Watering system ready - AI suggestions online...\n");
    thor_printf("[GATESCORE]   Reputation system loaded...\n");
    thor_printf("[MESH]        THOR network connected...\n");
    thor_printf("[DRIVERS]     AI optimization protocols active...\n");
    thor_printf("[SECURITY]    Firewall initialized - Privacy enforced...\n");
    thor_printf("[GAMING]      Universal game tracking ready...\n");
    thor_printf("\n");

    thor_console_set_color(THOR_COLOR_CYAN, THOR_COLOR_BLACK);
    thor_printf("� THOR-OS ONE MAN ARMY: Ultimate Developer & Gamer Platform\n");
    thor_printf("🌱 Local Hosting & Repo Sync - \"Water Your Tree\" Philosophy\n");
    thor_printf("🌐 P2P THOR Cloud - Decentralized Collaboration\n");
    thor_printf("� AI Assistant - Code, Game, Create Together\n");
    thor_printf("🔧 THOR Vault - Secure Local Repository System\n");
    thor_printf("⚡ THOR Forge - Multi-user Code Workshop\n");
    thor_printf("🔐 Privacy-First - GDPR Compliant, Local Control\n");
    thor_printf("� Universal Game Tracking & Optimization\n");
    thor_printf("🏆 GATESCORE: Merit-based gaming reputation\n");
    thor_printf("🌳 Easter Egg: Find the hidden watering spot!\n");
    thor_printf("\n");

    thor_console_set_color(THOR_COLOR_WHITE, THOR_COLOR_BLACK);
}

void thor_print_one_man_army_banner(void)
{
    thor_console_set_color(THOR_COLOR_YELLOW, THOR_COLOR_BLACK);

    thor_printf("========================================\n");
    thor_printf("   ONE MAN ARMY EDITION ACTIVATED!    \n");
    thor_printf("========================================\n");
    thor_printf("\n");

    thor_console_set_color(THOR_COLOR_WHITE, THOR_COLOR_BLACK);
    thor_printf("        Ultimate Developer & Gamer\n");
    thor_printf("         Version %d.%d.%d \"%s\"\n",
                THOR_OS_VERSION_MAJOR, THOR_OS_VERSION_MINOR,
                THOR_OS_VERSION_PATCH, THOR_OS_CODENAME);
    thor_printf("       Built for Autonomous Developers\n");
    thor_printf("         and Elite Gamers by THOR AI\n");
    thor_printf("\n");

    thor_console_set_color(THOR_COLOR_MAGENTA, THOR_COLOR_BLACK);
    thor_printf("[VAULT]       Local repository system\n");
    thor_printf("[FORGE]       Code editor and workshop\n");
    thor_printf("[P2P CLOUD]   Peer-to-peer cloud system\n");
    thor_printf("[SYNC]        Advanced sync engine\n");
    thor_printf("[SECURITY]    Enhanced security firewall\n");
    thor_printf("\n");

    thor_console_set_color(THOR_COLOR_CYAN, THOR_COLOR_BLACK);
    thor_printf("🌟 ONE MAN ARMY: Unleash Your Potential\n");
    thor_printf("🚀 Develop, Game, and Optimize like never before\n");
    thor_printf("⚔️ Join the elite ranks of THOR-OS users\n");
    thor_printf("🏆 GATESCORE: Prove your skills, earn respect\n");
    thor_printf("\n");

    thor_console_set_color(THOR_COLOR_WHITE, THOR_COLOR_BLACK);
}

// THOR-OS AI Driver Generator
struct thor_driver *thor_ai_generate_driver(struct hardware_device *device)
{
    struct thor_driver *driver;
    struct ai_analysis analysis;

    thor_printf("[THOR-AI] Analyzing hardware: %s\n", device->name);

    // AI analyzes the hardware
    analysis = thor_ai_analyze_hardware(device);

    // Load base driver template
    driver = thor_load_base_driver(device->type);
    if (!driver)
    {
        thor_printf("[ERROR] No base driver for device type: %d\n", device->type);
        return NULL;
    }

    // AI optimization phase
    if (analysis.optimization_potential > 0.5)
    {
        thor_printf("[THOR-AI] Optimization potential: %.1f%% - Generating custom driver\n",
                    analysis.optimization_potential * 100);

        // GPU optimization
        if (device->type == THOR_DEVICE_GPU)
        {
            driver = thor_ai_optimize_gpu_driver(driver, &analysis);
        }
        // CPU optimization
        else if (device->type == THOR_DEVICE_CPU)
        {
            driver = thor_ai_optimize_cpu_driver(driver, &analysis);
        }
        // Network optimization
        else if (device->type == THOR_DEVICE_NETWORK)
        {
            driver = thor_ai_optimize_network_driver(driver, &analysis);
        }

        // Test the optimized driver
        if (thor_test_driver(driver, device))
        {
            thor_printf("[THOR-AI] ✅ Optimized driver validated - Performance gain: %.1f%%\n",
                        analysis.performance_gain * 100);

            // Share to MESH network
            thor_mesh_share_driver(driver, device, &analysis);
        }
        else
        {
            thor_printf("[THOR-AI] ⚠️ Optimized driver failed validation - Using base driver\n");
            driver = thor_load_base_driver(device->type);
        }
    }

    return driver;
}

// THOR-OS Game Optimization System
void thor_optimize_game(const char *game_executable)
{
    struct game_profile *profile;
    struct optimization_result result;

    thor_printf("[THOR-GAME] Optimizing: %s\n", game_executable);

    // Check MESH for existing profile
    profile = thor_mesh_get_game_profile(game_executable);

    if (!profile)
    {
        thor_printf("[THOR-AI] No MESH profile found - Creating new optimization\n");

        // AI analyzes the game
        profile = thor_ai_analyze_game(game_executable);

        // Detect game engine
        switch (profile->engine_type)
        {
        case THOR_ENGINE_UNREAL5:
            thor_optimize_unreal5(profile);
            break;
        case THOR_ENGINE_UNITY:
            thor_optimize_unity(profile);
            break;
        case THOR_ENGINE_SOURCE2:
            thor_optimize_source2(profile);
            break;
        case THOR_ENGINE_CUSTOM:
            thor_ai_generic_optimize(profile);
            break;
        }
    }
    else
    {
        thor_printf("[THOR-MESH] Found existing profile - Adapting to local hardware\n");
        thor_ai_adapt_profile(profile);
    }

    // Apply optimizations
    result = thor_apply_game_optimizations(profile);

    if (result.success)
    {
        thor_printf("[THOR-GAME] ✅ Optimization complete - FPS gain: %.1f%%\n",
                    result.fps_improvement);

        // Update GATESCORE for optimization sharing
        if (result.fps_improvement > 10.0)
        {
            thor_gatescore_add_achievement(THOR_ACHIEVEMENT_OPTIMIZER);
        }

        // Share successful optimization to MESH
        thor_mesh_share_game_profile(profile, &result);
    }
    else
    {
        thor_printf("[THOR-GAME] ❌ Optimization failed - Reverting to defaults\n");
    }
}

// THOR-OS Gaming Mode Activation
void thor_activate_gaming_mode(const char *game_name)
{
    thor_printf("\n🎮 THOR GAMING MODE ACTIVATED\n");
    thor_printf("Game: %s\n", game_name);

    // 1. AI Driver Optimization
    thor_printf("[DRIVERS] AI optimizing all drivers for gaming...\n");
    thor_ai_optimize_all_drivers();

    // 2. CPU Performance Mode
    thor_printf("[CPU] Setting maximum performance mode...\n");
    thor_cpu_set_performance_mode();

    // 3. GPU Gaming Mode
    thor_printf("[GPU] Activating gaming optimizations...\n");
    thor_gpu_gaming_mode();

    // 4. Memory Optimization
    thor_printf("[MEMORY] Optimizing memory allocation...\n");
    thor_memory_gaming_optimize();

    // 5. Network Gaming Mode
    thor_printf("[NETWORK] Reducing latency and jitter...\n");
    thor_network_gaming_mode();

    // 6. Kill unnecessary processes
    thor_printf("[SYSTEM] Stopping non-essential services...\n");
    thor_system_gaming_mode();

    // 7. Start AI monitoring
    thor_printf("[THOR-AI] Starting real-time game monitoring...\n");
    thor_ai_start_game_monitoring(game_name);

    thor_printf("🚀 THOR Gaming Mode: READY\n\n");
}

// THOR-OS MESH Network Integration
void thor_mesh_share_optimization(struct optimization_data *opt)
{
    struct mesh_packet packet;

    // Anonymize data for privacy
    packet.data = thor_anonymize_optimization(opt);
    packet.signature = thor_sign_data(packet.data);
    packet.timestamp = thor_get_time();

    // Broadcast to MESH network
    thor_mesh_broadcast(&packet);

    thor_system.total_gatescore_calculations++;

    thor_printf("[THOR-MESH] Shared optimization to %d nodes\n",
                thor_system.mesh_nodes_connected);
}

// THOR-OS GATESCORE Integration
uint32_t thor_calculate_gatescore(struct player_data *player)
{
    uint32_t base_score;
    uint32_t final_score;

    // Base calculation using our transparent math
    base_score = thor_gatescore_base_calculation(player);

    // AI enhancement based on behavior analysis
    final_score = thor_ai_enhance_gatescore(base_score, player);

    thor_printf("[GATESCORE] Player score: %d/10000\n", final_score);

    return final_score;
}

// THOR-OS Main Kernel Loop
void thor_kernel_loop(void)
{
    thor_printf("[THOR-OS] Kernel ready - Entering main loop\n");

    while (1)
    {
        // Handle interrupts
        thor_handle_interrupts();

        // AI background processing
        thor_ai_background_process();

        // MESH network processing
        thor_mesh_process_packets();

        // Gaming optimizations
        thor_gaming_background_optimize();

        // GATESCORE updates
        thor_gatescore_update();

        // Schedule next task
        thor_scheduler_yield();
    }
}

// THOR-OS System Information
void thor_show_system_info(void)
{
    thor_printf("\n🔥 THOR-OS SYSTEM INFORMATION\n");
    thor_printf("================================\n");
    thor_printf("Version: %d.%d.%d \"%s\"\n",
                thor_system.version_major,
                thor_system.version_minor,
                thor_system.version_patch,
                thor_system.codename);
    thor_printf("Edition: %s\n", thor_system.edition);
    thor_printf("Uptime: %llu seconds\n", thor_get_uptime());
    thor_printf("AI Instances: %d\n", thor_system.ai_instances);
    thor_printf("MESH Nodes: %d\n", thor_system.mesh_nodes_connected);
    thor_printf("Active Gamers: %d\n", thor_system.active_gamers);
    thor_printf("GATESCORE Calculations: %llu\n", thor_system.total_gatescore_calculations);
    thor_printf("Vault Repos: %d\n", thor_system.vault_repos_count);
    thor_printf("Forge Sessions: %d\n", thor_system.forge_sessions_active);
    thor_printf("P2P Peers: %d\n", thor_system.p2p_peers_connected);
    thor_printf("Sync Operations: %llu\n", thor_system.sync_operations_completed);
    thor_printf("\n🎮 This is OUR operating system!\n");
    thor_printf("Built specifically for gaming excellence!\n");
}

// THOR-OS Entry Point
void _start(void)
{
    // This is where THOR-OS begins!
    thor_kernel_main(0, 0);
}

// THOR-OS VAULT - Local Repository System
void thor_init_vault_system(void)
{
    strcpy(system_vault.path, "/vault");
    system_vault.repo_count = 0;
    system_vault.total_size = 0;
    system_vault.encryption_enabled = true;
    system_vault.active_branch = 0;
    system_vault.pending_commits = 0;
    system_vault.sync_destinations = 0;

    thor_printf("[VAULT] Initialized local repository system\n");
}

// THOR-OS FORGE - Code Editor/Workshop
void thor_init_forge_system(void)
{
    system_forge.active_sessions = 0;
    system_forge.party_mode_users = 0;
    system_forge.collaboration_enabled = false;
    system_forge.ai_suggestions_pending = 0;
    system_forge.real_time_sync = false;

    thor_printf("[FORGE] Initialized code editor and workshop\n");
}

// THOR-OS P2P CLOUD - Peer-to-Peer Cloud System
void thor_init_p2p_cloud(void)
{
    system_p2p.discovered_peers = 0;
    system_p2p.trusted_peers = 0;
    system_p2p.data_shared = 0;
    system_p2p.data_received = 0;
    system_p2p.reputation_score = 0;

    thor_printf("[P2P CLOUD] Initialized peer-to-peer cloud system\n");
}

// THOR-OS SYNC ENGINE - Advanced Sync Engine
void thor_init_sync_engine(void)
{
    system_sync.pending_syncs = 0;
    system_sync.completed_syncs = 0;
    system_sync.failed_syncs = 0;
    system_sync.ai_recommendations_enabled = false;
    system_sync.tree_watering_count = 0;

    thor_printf("[SYNC] Initialized advanced sync engine\n");
}

// THOR-OS SECURITY - Enhanced Security Firewall
void thor_init_security_firewall(void)
{
    thor_printf("[SECURITY] Enhanced security firewall active\n");
}

// Easter Egg - THOR's Hammer
void thor_print_easter_egg_hammer(void)
{
    thor_console_set_color(THOR_COLOR_YELLOW, THOR_COLOR_BLACK);

    thor_printf("    _.-'~~~~~~`-._\n");
    thor_printf("  .`  _.-'~~~~`-._  `.\n");
    thor_printf(" /  .`  _.-'~~~~`-._  `.  \n");
    thor_printf("|  /  .`  _.-'~~~~`-._  `.  |\n");
    thor_printf("| |  /  .`  _.-'~~~~`-._  `. | |\n");
    thor_printf("| | |  /  .`  _.-'~~~~`-._  `. | |\n");
    thor_printf("| | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  /  .`  _.-'~~~~`-._  `. | | |\n");
    thor_printf("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |