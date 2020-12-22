import hypothesis.strategies as st
import pkg_resources
import pytest
from hypothesis import given, settings
from py4j.protocol import Py4JNetworkError

from negmas import (
    GeniusNegotiator,
    AspirationNegotiator,
    genius_bridge_is_running,
    init_genius_bridge,
    load_genius_domain,
    load_genius_domain_from_folder,
    AgentK,
    Yushu,
    Nozomi,
    IAMhaggler,
    AgentX,
    YXAgent,
    Caduceus,
    ParsCat,
    ParsAgent,
    PonPokoAgent,
    RandomDance,
    BetaOne,
    MengWan,
    AgreeableAgent2018,
    Rubick,
    CaduceusDC16,
    Terra,
    AgentHP2,
    GrandmaAgent,
    Ngent,
    Atlas32016,
    MyAgent,
    Farma,
    PokerFace,
    XianFaAgent,
    PhoenixParty,
    AgentBuyong,
    Kawaii,
    Atlas3,
    AgentYK,
    KGAgent,
    E2Agent,
    Group2,
    WhaleAgent,
    DoNA,
    AgentM,
    TMFAgent,
    MetaAgent,
    TheNegotiatorReloaded,
    OMACagent,
    AgentLG,
    CUHKAgent,
    ValueModelAgent,
    NiceTitForTat,
    TheNegotiator,
    AgentK2,
    BRAMAgent,
    IAMhaggler2011,
    Gahboninho,
    HardHeaded,
)
from negmas.genius import GeniusBridge


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_genius_bridge_cleaning():
    GeniusBridge().clean()


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_genius_does_not_freeze():
    from negmas.inout import load_genius_domain_from_folder
    from negmas.genius import GeniusNegotiator
    from pathlib import Path

    folder_name = pkg_resources.resource_filename(
        "negmas", resource_name="tests/data/cameradomain"
    )
    mechanism, ufuns, issues = load_genius_domain_from_folder(folder_name, time_limit=1)
    a1 = GeniusNegotiator(
        java_class_name="agents.anac.y2017.ponpokoagent.PonPokoAgent",
        domain_file_name=f"{folder_name}/{mechanism.name}.xml",
        utility_file_name=ufuns[0]["ufun_name"],
    )

    a2 = GeniusNegotiator(
        java_class_name="agents.anac.y2016.yxagent.YXAgent",
        domain_file_name=f"{folder_name}/{mechanism.name}.xml",
        utility_file_name=ufuns[1]["ufun_name"],
    )

    mechanism.add(a1)
    mechanism.add(a2)
    print(mechanism.run())
    print(a1.ufun.__call__(mechanism.agreement), a2.ufun.__call__(mechanism.agreement))
    GeniusBridge().clean()


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_old_agent():
    from negmas.inout import load_genius_domain_from_folder
    from negmas.genius import GeniusNegotiator
    from pathlib import Path

    folder_name = pkg_resources.resource_filename(
        "negmas", resource_name="tests/data/cameradomain"
    )
    mechanism, ufuns, issues = load_genius_domain_from_folder(folder_name, time_limit=1)
    a1 = GeniusNegotiator(
        java_class_name="agents.anac.y2012.AgentLG.AgentLG",
        domain_file_name=f"{folder_name}/{mechanism.name}.xml",
        utility_file_name=ufuns[0]["ufun_name"],
    )

    a2 = GeniusNegotiator(
        java_class_name="agents.anac.y2016.yxagent.YXAgent",
        domain_file_name=f"{folder_name}/{mechanism.name}.xml",
        utility_file_name=ufuns[1]["ufun_name"],
    )

    mechanism.add(a1)
    mechanism.add(a2)
    print(mechanism.run())
    print(a1.ufun.__call__(mechanism.agreement), a2.ufun.__call__(mechanism.agreement))
    GeniusBridge().clean()


# def test_init_genius_bridge():
#     if not genius_bridge_is_running():
#         init_genius_bridge()
#     assert genius_bridge_is_running()


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
@settings(max_examples=20, deadline=50000)
@given(
    agent_name1=st.sampled_from(GeniusNegotiator.robust_negotiators()),
    agent_name2=st.sampled_from(GeniusNegotiator.robust_negotiators()),
    single_issue=st.booleans(),
    keep_issue_names=st.booleans(),
    keep_value_names=st.booleans(),
)
def test_genius_agents_run_using_hypothesis(
    agent_name1, agent_name2, single_issue, keep_issue_names, keep_value_names,
):
    from negmas import convert_genius_domain_from_folder

    # TODO remove this limitation.
    if keep_issue_names != keep_value_names:
        return
    src = pkg_resources.resource_filename("negmas", resource_name="tests/data/Laptop")
    dst = pkg_resources.resource_filename(
        "negmas", resource_name="tests/data/LaptopConv1D"
    )
    if single_issue:
        assert convert_genius_domain_from_folder(
            src_folder_name=src,
            dst_folder_name=dst,
            force_single_issue=True,
            cache_and_discretize_outcomes=True,
            n_discretization=10,
        )
        base_folder = dst
    else:
        base_folder = src
    neg, agent_info, issues = load_genius_domain_from_folder(
        base_folder,
        keep_issue_names=keep_issue_names,
        keep_value_names=keep_value_names,
        time_limit=1,
    )
    if neg is None:
        raise ValueError(f"Failed to lead domain from {base_folder}")
    a1 = GeniusNegotiator(
        java_class_name=agent_name1,
        ufun=agent_info[0]["ufun"],
        keep_issue_names=keep_issue_names,
        keep_value_names=keep_value_names,
    )
    a2 = GeniusNegotiator(
        java_class_name=agent_name2,
        ufun=agent_info[1]["ufun"],
        keep_issue_names=keep_issue_names,
        keep_value_names=keep_value_names,
    )
    neg._enable_callbacks = True
    neg.add(a1)
    neg.add(a2)
    neg.run()
    GeniusBridge().clean()


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_genius_agent_gets_ufun():
    agents = ["agents.anac.y2015.Atlas3.Atlas3", "agents.anac.y2015.AgentX.AgentX"]
    base_folder = pkg_resources.resource_filename(
        "negmas", resource_name="tests/data/Laptop"
    )
    neg, agent_info, issues = load_genius_domain_from_folder(
        base_folder, keep_issue_names=True, keep_value_names=True,
    )
    a1 = GeniusNegotiator(
        java_class_name="agents.anac.y2015.Atlas3.Atlas3",
        domain_file_name=base_folder + "/Laptop-C-domain.xml",
        utility_file_name=base_folder + f"/Laptop-C-prof1.xml",
        keep_issue_names=True,
        keep_value_names=True,
    )
    assert a1.ufun is not None
    assert not a1._temp_ufun_file
    assert not a1._temp_domain_file
    a2 = GeniusNegotiator(
        java_class_name="agents.anac.y2015.Atlas3.Atlas3",
        domain_file_name=base_folder + "/Laptop-C-domain.xml",
        ufun=agent_info[0]["ufun"],
        keep_issue_names=True,
        keep_value_names=True,
    )
    neg.add(a1)
    neg.add(a2)
    assert a2.ufun is not None
    assert a2._temp_ufun_file
    assert not a2._temp_domain_file
    neg.run()
    GeniusBridge().clean()


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_genius_agents_run_example():
    from random import randint

    agents = ["agents.anac.y2015.Atlas3.Atlas3", "agents.anac.y2015.AgentX.AgentX"]
    for _ in range(5):
        agent_name1 = agents[randint(0, 1)]
        agent_name2 = agents[randint(0, 1)]
        print(f"{agent_name1} - {agent_name2}")
        utils = (1, 2)

        base_folder = pkg_resources.resource_filename(
            "negmas", resource_name="tests/data/Laptop"
        )
        neg, agent_info, issues = load_genius_domain_from_folder(
            base_folder, keep_issue_names=True, keep_value_names=True,
        )
        if neg is None:
            raise ValueError(f"Failed to lead domain from {base_folder}")
        atlas = GeniusNegotiator(
            java_class_name=agent_name1,
            domain_file_name=base_folder + "/Laptop-C-domain.xml",
            utility_file_name=base_folder + f"/Laptop-C-prof{utils[0]}.xml",
            keep_issue_names=True,
            keep_value_names=True,
        )
        agentx = GeniusNegotiator(
            java_class_name=agent_name2,
            domain_file_name=base_folder + "/Laptop-C-domain.xml",
            utility_file_name=base_folder + f"/Laptop-C-prof{utils[1]}.xml",
            keep_issue_names=True,
            keep_value_names=True,
        )
        neg.add(atlas)
        neg.add(agentx)
        neg.run()

    GeniusBridge().clean()


def do_test_genius_agent(AgentClass):
    print(f"Running {AgentClass.__name__}")
    base_folder = pkg_resources.resource_filename(
        "negmas", resource_name="tests/data/Laptop"
    )

    def do_run(
        opponent_ufun,
        agent_ufun,
        agent_starts,
        opponent_type=AspirationNegotiator,
        n_steps=10,
        time_limit=20,
        outcome_type=dict,
    ):
        neg, agent_info, issues = load_genius_domain_from_folder(
            base_folder,
            keep_issue_names=outcome_type == dict,
            keep_value_names=outcome_type == dict,
            time_limit=time_limit,
            n_steps=n_steps,
            outcome_type=outcome_type,
        )
        if neg is None:
            raise ValueError(f"Failed to load domain from {base_folder}")
        if isinstance(opponent_type, GeniusNegotiator):
            opponent = opponent_type(
                ufun=agent_info[opponent_ufun]["ufun"],
                keep_issue_names=outcome_type == dict,
                keep_issue_values=outcome_type == dict,
            )
        else:
            opponent = opponent_type(ufun=agent_info[opponent_ufun]["ufun"])
        theagent = AgentClass(ufun=agent_info[agent_ufun]["ufun"])
        if agent_starts:
            neg.add(theagent)
            neg.add(opponent)
        else:
            neg.add(opponent)
            neg.add(theagent)
        return neg.run()

    # check that it will get to an agreement sometimes if the same ufun
    # is used for both agents
    n_trials = 5
    got_agreement = False
    for starts in (False, True):
        for _ in range(n_trials):
            neg = do_run(0, 0, starts)
            if neg.agreement is not None:
                got_agreement = True
                break

    # check that it can run without errors with two different ufuns
    for outcome_type in (dict, tuple):
        for opponent_type in (AspirationNegotiator, Atlas3):
            for starts in (True, False):
                for n_steps, time_limit in ((10, 10), (10, float("inf")), (None, 10)):
                    for ufuns in ((0, 1), (1, 0)):
                        try:
                            do_run(
                                ufuns[0],
                                ufuns[1],
                                starts,
                                opponent_type,
                                n_steps=n_steps,
                                time_limit=time_limit,
                                outcome_type=outcome_type,
                            )
                        except Exception as e:
                            print(
                                f"{AgentClass.__name__} FAILED against {opponent_type.__name__}"
                                f" going {'first' if starts else 'last'} ({n_steps} steps with "
                                f"{time_limit} limit taking ufun {ufuns[1]})."
                            )
                            raise e

    if not got_agreement:
        assert (
            False
        ), f"{AgentClass.__name__}: failed to get an agreement in {n_trials} trials even using the same ufun"

    GeniusBridge().clean()


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_AgentX():
    do_test_genius_agent(AgentX)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_YXAgent():
    do_test_genius_agent(YXAgent)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_Caduceus():
    do_test_genius_agent(Caduceus)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_ParsCat():
    do_test_genius_agent(ParsCat)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_ParsAgent():
    do_test_genius_agent(ParsAgent)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_PonPokoAgent():
    do_test_genius_agent(PonPokoAgent)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_RandomDance():
    do_test_genius_agent(RandomDance)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_GrandmaAgent():
    do_test_genius_agent(GrandmaAgent)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_Ngent():
    do_test_genius_agent(Ngent)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_Atlas32016():
    do_test_genius_agent(Atlas32016)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_MyAgent():
    do_test_genius_agent(MyAgent)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_Farma():
    do_test_genius_agent(Farma)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_PokerFace():
    do_test_genius_agent(PokerFace)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_XianFaAgent():
    do_test_genius_agent(XianFaAgent)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_PhoenixParty():
    do_test_genius_agent(PhoenixParty)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_AgentBuyong():
    do_test_genius_agent(AgentBuyong)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_Kawaii():
    do_test_genius_agent(Kawaii)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_Atlas3():
    do_test_genius_agent(Atlas3)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_AgentYK():
    do_test_genius_agent(AgentYK)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_Group2():
    do_test_genius_agent(Group2)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_WhaleAgent():
    do_test_genius_agent(WhaleAgent)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_DoNA():
    do_test_genius_agent(DoNA)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_AgentM():
    do_test_genius_agent(AgentM)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_TMFAgent():
    do_test_genius_agent(TMFAgent)


# @pytest.mark.skipif(
#     condition=not genius_bridge_is_running(),
#     reason="No Genius Bridge, skipping genius-agent tests",
# )
# def test_MetaAgent():
#     do_test_genius_agent(MetaAgent)


# @pytest.mark.skipif(
#     condition=not genius_bridge_is_running(),
#     reason="No Genius Bridge, skipping genius-agent tests",
# )
# def test_TheNegotiatorReloaded():
#     do_test_genius_agent(TheNegotiatorReloaded)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_OMACagent():
    do_test_genius_agent(OMACagent)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_AgentLG():
    do_test_genius_agent(AgentLG)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_CUHKAgent():
    do_test_genius_agent(CUHKAgent)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_ValueModelAgent():
    do_test_genius_agent(ValueModelAgent)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_NiceTitForTat():
    do_test_genius_agent(NiceTitForTat)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_TheNegotiator():
    do_test_genius_agent(TheNegotiator)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_AgentK2():
    do_test_genius_agent(AgentK2)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_BRAMAgent():
    do_test_genius_agent(BRAMAgent)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_IAMhaggler2011():
    do_test_genius_agent(IAMhaggler2011)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_Gahboninho():
    do_test_genius_agent(Gahboninho)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_HardHeaded():
    do_test_genius_agent(HardHeaded)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_AgentK():
    do_test_genius_agent(AgentK)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_Yushu():
    do_test_genius_agent(Yushu)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_Nozomi():
    do_test_genius_agent(Nozomi)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_IAMhaggler():
    do_test_genius_agent(IAMhaggler)


@pytest.mark.skipif(
    condition=not genius_bridge_is_running(),
    reason="No Genius Bridge, skipping genius-agent tests",
)
def test_Terra():
    do_test_genius_agent(Terra)


#### agents after this line are not very robust

# @pytest.mark.skipif(
#     condition=not genius_bridge_is_running(),
#     reason="No Genius Bridge, skipping genius-agent tests",
# )
# def test_Rubick():
#     do_test_genius_agent(Rubick)
#
#
# @pytest.mark.skipif(
#     condition=not genius_bridge_is_running(),
#     reason="No Genius Bridge, skipping genius-agent tests",
# )
# def test_CaduceusDC16():
#     do_test_genius_agent(CaduceusDC16)
#
#
# @pytest.mark.skipif(
#     condition=not genius_bridge_is_running(),
#     reason="No Genius Bridge, skipping genius-agent tests",
# )
# def test_BetaOne():
#     do_test_genius_agent(BetaOne)
#
#
# @pytest.mark.skipif(
#     condition=not genius_bridge_is_running(),
#     reason="No Genius Bridge, skipping genius-agent tests",
# )
# def test_AgreeableAgent2018():
#     do_test_genius_agent(AgreeableAgent2018)
#
#
# @pytest.mark.skipif(
#     condition=not genius_bridge_is_running(),
#     reason="No Genius Bridge, skipping genius-agent tests",
# )
# def test_AgentHP2():
#     do_test_genius_agent(AgentHP2)
#
#
# @pytest.mark.skipif(
#     condition=not genius_bridge_is_running(),
#     reason="No Genius Bridge, skipping genius-agent tests",
# )
# def test_KGAgent():
#     do_test_genius_agent(KGAgent)
#
#
# @pytest.mark.skipif(
#     condition=not genius_bridge_is_running(),
#     reason="No Genius Bridge, skipping genius-agent tests",
# )
# def test_MengWan():
#     do_test_genius_agent(MengWan)

# @pytest.mark.skipif(
#     condition=not genius_bridge_is_running(),
#     reason="No Genius Bridge, skipping genius-agent tests",
# )
# def test_E2Agent():
#     do_test_genius_agent(E2Agent)

if __name__ == "__main__":
    pytest.main(args=[__file__])
