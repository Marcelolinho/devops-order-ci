from app import cli


def test_cli_calcula_total_com_argumentos(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        [
            "prog",
            "--preco",
            "100",
            "--quantidade",
            "2",
            "--desconto",
            "10",
            "--cupom",
            "DEVOPS10",
        ],
    )

    cli.main()

    saida = capsys.readouterr().out.strip()
    assert saida == "176.90"
