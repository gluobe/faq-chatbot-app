import unittest
import databank


class Testdatabank(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_sleutels(self):
        self.assertIsInstance(databank.get_sleutels(), list)

    def test_get_titels(self):
        self.assertIsInstance(databank.get_titels(), list)

    def test_get_links(self):
        self.assertIsInstance(databank.get_links(), list)

    def test_get_antwoorden(self):
        self.assertIsInstance(databank.get_antwoorden(), list)

    def test_get_titel_en_links(self):
        self.assertIsInstance(databank.get_titel_en_links(), str)

    def test_get_antwoord(self):
        self.assertEqual(databank.get_antwoord("hallo"), "hallo, hoe gaat het?")
        self.assertEqual(databank.get_antwoord("help"), "hulp nodig?")
        self.assertEqual(databank.get_antwoord("status"), "De status van de server is \"Online\".")
        self.assertEqual(databank.get_antwoord("lijst"), "hier is de lijst van de keywoorden:")
        self.assertEqual(databank.get_antwoord("aan"), "De server staat aan")
        self.assertEqual(databank.get_antwoord("uit"), "De server staat uit")
        self.assertEqual(databank.get_antwoord("documentatie"), " documentatie vind je op volgende link: ")

    def test_get_link(self):
        self.assertEqual(databank.get_link("Python", "documentatie"), "http://tdc-www.harvard.edu/Python.pdf")
        self.assertEqual(databank.get_link("ecs", "documentatie"), "https://docs.aws.amazon.com/ecs/index.html#lang/en_us")
        self.assertEqual(databank.get_link("ec2", "documentatie"), "https://docs.aws.amazon.com/ec2/index.html#lang/en_us")
        self.assertEqual(databank.get_link("ecr", "documentatie"), "https://docs.aws.amazon.com/ecr/index.html#lang/en_us")
        self.assertEqual(databank.get_link("s3", "documentatie"), "https://docs.aws.amazon.com/s3/index.html#lang/en_us")
        self.assertEqual(databank.get_link("codebuild", "documentatie"), "https://docs.aws.amazon.com/codebuild/index.html#lang/en_us")
        self.assertEqual(databank.get_link("codepipeline", "documentatie"), "https://docs.aws.amazon.com/codepipeline/index.html#lang/en_us")
        self.assertEqual(databank.get_link("docker", "documentatie"), "https://docs.docker.com/")
        self.assertEqual(databank.get_link("cloudformation", "documentatie"), "https://docs.aws.amazon.com/cloudformation/index.html")
        self.assertEqual(databank.get_link("terraform", "documentatie"), "https://www.terraform.io/intro/index.html")
        self.assertEqual(databank.get_link("kubernetes", "documentatie"), "https://kubernetes.io/docs/home/")
        self.assertEqual(databank.get_link("jenkins", "documentatie"), "https://jenkins.io/doc/")

    def test_vullen(self):
        self.assertEqual(databank.vullen(), False)


if __name__ == "__main__":
    unittest.main()
